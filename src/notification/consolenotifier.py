from logger import Logger
from notification.notify import Notifier


class Api(Notifier):

    @staticmethod
    def is_valid_config(config):
        return True

    def send_message(self, message, title=None):
        Logger().logger.info("{}: {}".format(title, message))

