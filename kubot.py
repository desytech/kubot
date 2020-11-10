import sched, time
import socket
import requests

from kucoin.client import Margin, User
from config.config import config
from logger import Logger
from datetime import datetime, timedelta
from notification.notify import Notifier
from notification.pushovernotifier import Api as PushoverNotifier
from notification.consolenotifier import Api as ConsoleNotifier
from coin import coin


class Scheduler(object):

    def __init__(self, coins=[], notificationapi=None):
        self.__client = Margin(config.api_key, config.api_secret, config.api_passphrase)
        self.__user = User(config.api_key, config.api_secret, config.api_passphrase)
        self.__notify = notificationapi if isinstance(notificationapi, Notifier) else None
        self.__lendable_coins = coins
        self.__scheduler = sched.scheduler(time.time, time.sleep)
        self.schedule_checks(config.interval)
        self.__scheduler.run()

    def push_message(self, message, title=None):
        self.__notify.send_message(message, title=title)

    def schedule_checks(self, interval):
        self.__scheduler.enter(interval, 1, self.schedule_checks, argument=(interval,))
        for coin in self.__lendable_coins:
            try:
                min_int_rate = self.get_min_daily_interest_rate(coin)
                self.check_active_loans(coin, min_int_rate)
                self.lend_loans(coin, min_int_rate)
                self.check_active_lendings(coin)
            except (socket.timeout, requests.exceptions.Timeout) as e:
                Logger().logger.error("Transport Exception occured: %s", e)

    def trim_to_precision(self, amount, precision):
        return amount - (amount % precision)

    def lend_loans(self, coin, min_int_rate):
        account_list = self.__user.get_account_list(coin.symbol, 'main')
        print(account_list)
        account = next((x for x in account_list if x['currency'] == coin.symbol), None)
        if account:
            available = int(float(account['available']))
            if available and available >= coin.precision:
                if min_int_rate >= config.minimum_rate:
                    rate = float(format(min_int_rate + config.charge, '.5f'))
                else:
                    rate = config.minimum_rate
                try:
                    available = self.trim_to_precision(available, coin.precision)
                    Logger().logger.info("creating order: {}: available: {} rate: {}".format(coin.symbol, str(available), str(rate)))
                    order_id = self.__client.create_lend_order(coin.symbol, str(available), str(rate), 28)
                    info = "Created Lend Order: %s, Amount: %s, Rate: %s" % (order_id, available, rate)
                    Logger().logger.info(info)
                    self.push_message(info, title="Create Lend Order")
                except Exception as e:
                    Logger().logger.error("failed to create lend order: %s", e)
            else:
                Logger().logger.info("Insufficient Amount on Main Account: %s", available)

    def check_active_loans(self, coin, min_int_rate):
        active_orders = self.__client.get_active_order(currency=coin.symbol)
        for a in active_orders.get('items'):
            daily_int_rate = float(a['dailyIntRate'])
            if daily_int_rate >= min_int_rate:
                cancel_lend_order = abs(daily_int_rate - min_int_rate) >= config.correction
            else:
                cancel_lend_order = True
            if len(items) > 1 or cancel_lend_order and not (daily_int_rate == config.minimum_rate and min_int_rate <= config.minimum_rate):
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


def main():
    notifier = ConsoleNotifier()
    if config.pushover_enable == "yes":
        notifier = PushoverNotifier(config.user_key, config.api_token)

    lendable_coins = coin.All()
    Scheduler(coins=lendable_coins, notificationapi=notifier)


if __name__ == "__main__":
    main()
