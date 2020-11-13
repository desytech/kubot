import sys
import sched, time
import socket
import requests
import signal

from kucoin.client import Margin, User
from config.config import config
from logger import Logger
from datetime import datetime, timedelta
from notification.notify import Notifier
from notification.pushovernotifier import Api as PushoverNotifier
from notification.consolenotifier import Api as ConsoleNotifier
from coin import coin


class Scheduler(object):

    def __init__(self, coins=[], notifiers=[]):
        self.__client = Margin(config.api_key, config.api_secret, config.api_passphrase)
        self.__user = User(config.api_key, config.api_secret, config.api_passphrase)
        self.__notifiers = []
        for n in notifiers:
            if not isinstance(n, Notifier):
                Logger().logger.warning("could not add notifier: %s" % n)
                continue
            self.__notifiers.append(n)
        self.__lendable_coins = coins
        self.__scheduler = sched.scheduler(time.time, time.sleep)
        self.__minimum_rate = config.minimum_rate
        self.schedule_checks(config.interval)

    def push_message(self, message, title=None):
        for notifier in self.__notifiers:
            notifier.send_message(message, title=title)

    def schedule_checks(self, interval):
        self.__scheduler.enter(interval, 1, self.schedule_checks, argument=(interval,))
        for coin in self.__lendable_coins:
            try:
                min_int_rate = self.get_min_daily_interest_rate(coin)
                min_int_rate_charge = float(format(min_int_rate + config.charge, '.5f'))
                if abs(min_int_rate_charge - self.__minimum_rate) >= config.correction:
                    self.__minimum_rate = min_int_rate_charge
                self.check_active_loans(coin, min_int_rate)
                self.lend_loans(coin, min_int_rate)
                self.check_active_lendings(coin)
            except (socket.timeout, requests.exceptions.Timeout) as e:
                Logger().logger.error("Transport Exception occured: %s", e)

    def run(self):
        self.__scheduler.run()

    def trim_to_precision(self, amount, precision):
        return amount - (amount % precision)

    def lend_loans(self, coin, min_int_rate):
        account_list = self.__user.get_account_list(coin.symbol, 'main')
        Logger().logger.info("account_list: %s", account_list)
        account = next((x for x in account_list if x['currency'] == coin.symbol), None)
        if account:
            available = int(float(account['available']))
            if available and available >= coin.precision:
                if min_int_rate >= self.__minimum_rate:
                    rate = float(format(min_int_rate + config.charge, '.5f'))
                else:
                    rate = self.__minimum_rate
                available = self.trim_to_precision(available, coin.precision)
                order_id = self.__client.create_lend_order(coin.symbol, str(available), str(rate), 28)
                self.push_message("Create Lend Order: %s, Amount: %s, Rate: %s" % (order_id, available, rate),
                    title="Create Lend Order")
            else:
                Logger().logger.info("Insufficient Amount on Main Account: %s", available)

    def check_active_loans(self, coin, min_int_rate):
        active_orders = self.__client.get_active_order(currency=coin.symbol)
        items = active_orders.get('items')
        for a in items:
            daily_int_rate = float(a['dailyIntRate'])

            if daily_int_rate >= min_int_rate:
                cancel_lend_order = abs(daily_int_rate - min_int_rate) >= config.correction
            else:
                cancel_lend_order = True

            if len(items) > 1 or cancel_lend_order and not (daily_int_rate == self.__minimum_rate and min_int_rate <= self.__minimum_rate):
                self.__client.cancel_lend_order(a['orderId'])
                Logger().logger.info("Cancel Lend Order: Amount: %s, DailyIntRate: %s, "
                                     "MinIntRate: %s, DiffRate: %s, Correction: %s",
                                     a['size'],
                                     daily_int_rate,
                                     min_int_rate,
                                     abs(daily_int_rate - min_int_rate),
                                     config.correction
                                     )

    def get_min_daily_interest_rate(self, coin):
        lending_market = self.__client.get_lending_market(coin.symbol)
        if lending_market:
            return float(lending_market[0]['dailyIntRate'])
        else:
            return config.default_interest

    def check_active_lendings(self, coin):
        active_list = self.__client.get_active_list(pageSize=50)
        if active_list and active_list['items']:
            utc_now = datetime.utcnow()
            dt = timedelta(seconds=config.interval).total_seconds()
            for a in active_list['items']:
                maturity_timestamp = a['maturityTime'] / 1000
                time_diff = (utc_now - (datetime.utcfromtimestamp(maturity_timestamp) - timedelta(a['term']))).total_seconds()
                if time_diff <= dt:
                    maturity_date = datetime.fromtimestamp(maturity_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    self.push_message("Create Active Lending: Amount: {}, DailyIntRate: {}, MaturityDate: {}, AccruedInterest: {}".format(
                        a['size'],
                        a['dailyIntRate'],
                        maturity_date,
                        a['accruedInterest'])
                    , title="Create Active Lending")


def set_signal_handler():
    def sigint_handler(signum, frame):
        print('catched sigint: user abort ... bye')
        sys.exit(0)
    signal.signal(signal.SIGINT, sigint_handler)


def main():
    set_signal_handler()

    lendable_coins = coin.All()

    notifiers = [
        ConsoleNotifier(),
        PushoverNotifier(config.user_key, config.api_token),
    ]

    Scheduler(coins=lendable_coins, notifiers=notifiers).run()


if __name__ == "__main__":
    main()
