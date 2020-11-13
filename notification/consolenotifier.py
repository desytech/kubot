from notification.notify import Notifier

class Api(Notifier):

    def send_message(self, message, title=None):
        print("{}: console: {}: {}".format(self, title, message))

