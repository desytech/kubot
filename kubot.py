import sched, time
import socket
import requests

import const
from kucoin.client import Margin, User
from config.config import config
from logger import Logger
from datetime import datetime, timedelta
from notification.pushovernotifier import Api as PushoverNotifier
from notification.consolenotifier import Api as ConsoleNotifier
from helper import convert_float_to_percentage, get_version


class Scheduler(object):

    def __init__(self, notifiers):
        self.__client = Margin(config.api_key, config.api_secret, config.api_passphrase)
        self.__user = User(config.api_key, config.api_secret, config.api_passphrase)
        self.__notifiers = notifiers
        self.__scheduler = sched.scheduler(time.time, time.sleep)
        self.__minimum_rate = config.minimum_rate
        self.schedule_checks(config.interval)
        self.__scheduler.run()

    def push_message(self, message, title=None):
        for notifier in self.__notifiers:
            notifier.send_message(message, title=title)

    def schedule_checks(self, interval):
        self.__scheduler.enter(interval, 1, self.schedule_checks, argument=(interval,))
        try:
            min_int_rate = self.get_min_daily_interest_rate()
            min_int_rate_charge = float(format(min_int_rate + config.charge, '.5f'))
            if min_int_rate_charge <= config.minimum_rate:
                self.__minimum_rate = config.minimum_rate
            elif self.__minimum_rate == const.DEFAULT_MIN_RATE or abs(min_int_rate_charge - self.__minimum_rate) >= config.correction:
                self.__minimum_rate = min_int_rate_charge
            self.check_active_loans(min_int_rate)
            self.lend_loans(min_int_rate)
            self.check_active_lendings()
        except (socket.timeout, requests.exceptions.Timeout) as e:
            Logger().logger.error("Transport Exception occurred: %s", e)
        except Exception as e:
            Logger().logger.error("Generic Error occurred: %s", e)

    def lend_loans(self, min_int_rate):
        account_list = self.__user.get_account_list('USDT', 'main')
        account = next((x for x in account_list if x['currency'] == 'USDT'), None)
        if account:
            available = int(float(account['available']))
            if const.MIN_LEND_SIZE <= available <= const.MAX_LEND_SIZE:
                if min_int_rate >= self.__minimum_rate:
                    rate = float(format(min_int_rate + config.charge, '.5f'))
                else:
                    rate = self.__minimum_rate
                result = self.__client.create_lend_order("USDT", str(available), str(rate), 28)
                self.push_message("OrderId: {}, Amount: {}, Rate: {}".format(result['orderId'], available, convert_float_to_percentage(rate)),
                                  title="Create Lend Order")
            else:
                Logger().logger.info("Insufficient Amount on Main Account: %s", available)

    def check_active_loans(self, min_int_rate):
        active_orders = self.__client.get_active_order(currency="USDT")
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
                                     convert_float_to_percentage(daily_int_rate),
                                     convert_float_to_percentage(min_int_rate),
                                     convert_float_to_percentage(abs(daily_int_rate - min_int_rate)),
                                     convert_float_to_percentage(config.correction)
                                     )

    def get_min_daily_interest_rate(self):
        lending_market = self.__client.get_lending_market("USDT")
        lending_market = lending_market['data'] if 'data' in lending_market else lending_market
        if lending_market:
            return float(lending_market[0]['dailyIntRate'])
        else:
            return config.default_interest

    def check_active_lendings(self):
        active_list = self.__client.get_active_list(pageSize=50)
        if active_list and active_list['items']:
            utc_now = datetime.utcnow()
            dt = timedelta(seconds=config.interval).total_seconds()
            for a in active_list['items']:
                maturity_timestamp = a['maturityTime'] / 1000
                time_diff = (utc_now - (datetime.utcfromtimestamp(maturity_timestamp) - timedelta(a['term']))).total_seconds()
                if time_diff <= dt:
                    maturity_date = datetime.fromtimestamp(maturity_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    self.push_message("Amount: {}, DailyIntRate: {}, MaturityDate: {}, AccruedInterest: {}".format(
                        a['size'],
                        convert_float_to_percentage(a['dailyIntRate']),
                        maturity_date,
                        a['accruedInterest'])
                    , title="Create Active Lending")


def main():
    notifiers = [
        ConsoleNotifier(),
    ]

    if PushoverNotifier.is_valid_key(config.user_key) and PushoverNotifier.is_valid_key(config.api_token):
        try:
            notifiers.append(PushoverNotifier(config.user_key, config.api_token))
        except Exception as e:
            Logger().logger.error("Error occurred initializing Pushover notifier: %s", e)

    Scheduler(notifiers=notifiers)


if __name__ == "__main__":
    main()
