import sched, time
import socket
import requests

import const
from database.models.base import db
from database.models.market import FundingMarket
from database.models.activeorder import ActiveLendOrder
from database.models.assets import LendingAssets
from kucoin.client import Margin, User
from config.config import config
from logger import Logger
from datetime import datetime, timedelta
from notification.pushovernotifier import PushoverNotifier
from notification.consolenotifier import ConsoleNotifier
from notification.slacknotifier import SlackNotifier
from helper import convert_float_to_percentage, get_version
from currencies.currency import Currency


class Scheduler(object):

    def __init__(self, notifiers, currencies):
        self.__client = Margin(config.api_key, config.api_secret, config.api_passphrase)
        self.__user = User(config.api_key, config.api_secret, config.api_passphrase)
        self.__notifiers = notifiers
        self.__currencies = currencies
        self.__scheduler = sched.scheduler(time.time, time.sleep)
        self.__minimum_rate = config.minimum_rate
        self.schedule_checks(config.interval)
        self.schedule_status_push(config.status_interval)
        self.__scheduler.run()

    def push_message(self, message, title=None):
        for notifier in self.__notifiers:
            notifier.send_message(message, title=title)

    def cleanup_database(self):
        time_delta = datetime.utcnow() - timedelta(days=90)
        FundingMarket.delete().where(FundingMarket.time < time_delta).execute()
        ActiveLendOrder.delete().where(ActiveLendOrder.time < time_delta).execute()
        LendingAssets.delete().where(LendingAssets.time < time_delta).execute()

    def schedule_status_push(self, interval):
        self.__scheduler.enter(interval, 1, self.schedule_status_push, argument=(interval,))

    def schedule_checks(self, interval):
        self.__scheduler.enter(interval, 1, self.schedule_checks, argument=(interval,))
        self.cleanup_database()
        for currency in self.__currencies:
            try:
                min_int_rate = self.get_min_daily_interest_rate(currency)
                min_int_rate_charge = float(format(min_int_rate + config.charge, '.5f'))
                if min_int_rate_charge <= config.minimum_rate:
                    self.__minimum_rate = config.minimum_rate
                elif self.__minimum_rate == const.DEFAULT_MIN_RATE or abs(min_int_rate_charge - self.__minimum_rate) >= config.correction:
                    self.__minimum_rate = min_int_rate_charge
                self.get_lending_assets(currency)
                self.check_active_loans(min_int_rate, currency)
                self.lend_loans(min_int_rate, currency)
                self.check_active_lendings(currency)
            except (socket.timeout, requests.exceptions.Timeout) as e:
                Logger().logger.error("Currency: %s, Transport Exception occurred: %s", currency.name, e)
            except Exception as e:
                Logger().logger.error("Currency: %s, Generic Error occurred: %s", currency.name, e)

    def get_lending_assets(self, currency):
        asset = self.__client.get_lend_record(currency=currency.name)
        lending_asset = LendingAssets(currency=currency.name, assets=asset)
        Logger().logger.info('%s rows saved into the lending assets table', lending_asset.save())

    def lend_loans(self, min_int_rate, currency):
        account_list = self.__user.get_account_list(currency.name, 'main')
        account_list = account_list['data'] if 'data' in account_list else account_list
        account = next((x for x in account_list if x['currency'] == currency.name), None)
        if account:
            available = int(float(account['available'])) - currency.reserved_amount
            if const.MIN_LEND_SIZE <= available <= const.MAX_LEND_SIZE:
                if min_int_rate >= self.__minimum_rate:
                    rate = float(format(min_int_rate + config.charge, '.5f'))
                else:
                    rate = self.__minimum_rate
                self.__client.create_lend_order(currency.name, str(available), str(rate), currency.term)
                self.push_message("Currency: {}, Amount: {}, Rate: {}".format(
                     currency.name, available, convert_float_to_percentage(rate)
                ), title="Create Lend Order")
            else:
                Logger().logger.info("Insufficient Amount on %s Main Account: %s. Reserved Amount: %s", currency.name, str(available), str(currency.reserved_amount))

    def check_active_loans(self, min_int_rate, currency):
        active_orders = self.__client.get_active_order(currency=currency.name)
        items = active_orders.get('items')

        for a in items:
            daily_int_rate = float(a['dailyIntRate'])

            if daily_int_rate >= min_int_rate:
                cancel_lend_order = abs(daily_int_rate - min_int_rate) >= config.correction
            else:
                cancel_lend_order = True

            if len(items) > 1 or cancel_lend_order and not (daily_int_rate == self.__minimum_rate and min_int_rate <= self.__minimum_rate):
                self.__client.cancel_lend_order(a['orderId'])
                Logger().logger.info("Cancel Lend Order: Currency: %s, Amount: %s, DailyIntRate: %s, "
                                     "MinIntRate: %s, DiffRate: %s, Correction: %s",
                                     currency.name,
                                     a['size'],
                                     convert_float_to_percentage(daily_int_rate),
                                     convert_float_to_percentage(min_int_rate),
                                     convert_float_to_percentage(abs(daily_int_rate - min_int_rate)),
                                     convert_float_to_percentage(config.correction)
                                     )

    def get_min_daily_interest_rate(self, currency):
        lending_market = self.__client.get_lending_market(currency.name)
        lending_market = lending_market['data'] if 'data' in lending_market else lending_market
        market = FundingMarket(currency=currency.name, market=lending_market)
        Logger().logger.info('%s rows saved into the funding market table', market.save())
        if lending_market:
            return float(lending_market[0]['dailyIntRate'])
        else:
            return config.default_interest

    def check_active_lendings(self, currency):
        current_page = 1
        page_size = 50
        active_list = self.__client.get_active_list(pageSize=page_size, currency=currency.name, currentPage=current_page)
        for page in range(current_page + 1, active_list['totalPage'] + 1):
            result = self.__client.get_active_list(pageSize=page_size, currency=currency.name, currentPage=page)
            active_list['items'].extend(result['items'])
        if active_list:
            if 'items' in active_list:
                active_order = ActiveLendOrder(currency=currency.name, items=active_list['items'])
                Logger().logger.info('%s rows saved into the active order table', active_order.save())
                if active_list['items']:
                    utc_now = datetime.utcnow()
                    dt = timedelta(seconds=config.interval).total_seconds()
                    for a in active_list['items']:
                        maturity_timestamp = a['maturityTime'] / 1000
                        time_diff = (utc_now - (datetime.utcfromtimestamp(maturity_timestamp) - timedelta(a['term']))).total_seconds()
                        if time_diff <= dt:
                            maturity_date = datetime.fromtimestamp(maturity_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                            self.push_message("Currency: {}, Amount: {}, DailyIntRate: {}, MaturityDate: {}, AccruedInterest: {}".format(
                                currency.name,
                                a['size'],
                                convert_float_to_percentage(a['dailyIntRate']),
                                maturity_date,
                                round(float(a['size']) * float(a['dailyIntRate']) * float(1 - const.LENDING_FEES) * a['term'], 2))
                            , title="Create Active Lending")


def try_add_notifier(notifier, current_notifiers):
    if notifier.is_valid_config(config):
        try:
            current_notifiers.append(notifier(config))
        except Exception as e:
            Logger().logger.error("Error occurred initializing notifier: %s", e)


def main():
    Logger().logger.info("Starting Kubot Version {} - "
                         "Config: Correction: {}, Default Interest: {}, Minimum Rate: {}, Charge: {}"
                         .format(get_version(),
                                 convert_float_to_percentage(config.correction),
                                 convert_float_to_percentage(config.default_interest),
                                 convert_float_to_percentage(config.minimum_rate),
                                 convert_float_to_percentage(config.charge)))

    # initialize database
    with db:
        db.create_tables([FundingMarket, ActiveLendOrder, LendingAssets])

    # initialize notifier systems
    notifiers = []
    try_add_notifier(ConsoleNotifier, notifiers)
    try_add_notifier(PushoverNotifier, notifiers)
    try_add_notifier(SlackNotifier, notifiers)
    Logger().logger.info(f"Configured Notifiers: {[notifier.__class__.__name__ for notifier in notifiers]}")

    # initialize configured currencies
    currencies = [Currency(currency) for currency in config.currencies]

    # start main scheduler process
    Scheduler(notifiers=notifiers, currencies=currencies)


if __name__ == "__main__":
    main()
