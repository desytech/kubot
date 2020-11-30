from logger import Logger
from notification.notify import Notifier


class Api(Notifier):

    def send_message(self, message, title=None):
        Logger().logger.info("{}: {}".format(title, message))

