import sched, time

from kucoin.client import Margin, User
from config.config import config


class Scheduler(object):
    def __init__(self):
        self.__client = Margin(config.api_key, config.api_secret, config.api_passphrase)
        self.__user = User(config.api_key, config.api_secret, config.api_passphrase)
        self.__scheduler = sched.scheduler(time.time, time.sleep)
        self.schedule_checks(60)
        self.__scheduler.run()

    def schedule_checks(self, interval):
        self.__scheduler.enter(interval, 1, self.schedule_checks, argument=(interval,))
        self.check_active_loans(self.get_min_daily_interest_rate())

    def check_active_loans(self, min_int_rate):
        active_orders = self.__client.get_active_order(currency="USDT")
        for a in active_orders.get('items'):
            daily_int_rate = float(a['dailyIntRate'])
            if abs(daily_int_rate - min_int_rate) >= config.correction:
                self.__client.cancel_lend_order(a['orderId'])
                account_list = self.__user.get_account_list('USDT', 'main')
                account = next((x for x in account_list if x['currency'] == 'USDT'), None)
                if account:
                    available = int(float(account['available']))
                    if available:
                        if min_int_rate >= config.minimum_rate:
                            rate = min_int_rate + config.charge
                        else:
                            rate = config.minimum_rate
                        self.__client.create_lend_order('USDT', str(available), str(rate), 28)

    def get_min_daily_interest_rate(self):
        lending_market = self.__client.get_lending_market("USDT")
        if lending_market:
            return float(lending_market[0]['dailyIntRate'])
        else:
            return config.default_interest


def main():
    Scheduler()


if __name__ == "__main__":
    main()
