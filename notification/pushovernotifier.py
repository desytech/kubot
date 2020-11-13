from logger import Logger
from notification.notify import Notifier
from pushover import Client


class DummyApi(Notifier):

    def __init__(self, logger):
        self.logger = logger
        self.log_dummy_warning = True

    def send_message(self, message, title=None):
        self.warn_once_and_drop(message, title)

    def warn_once_and_drop(self, message, title=None):
        if self.log_dummy_warning:
            self.logger.warning("{}: no client: could not send: message='{}' title='{}'; only logged once".format(self, message, title))
            self.log_dummy_warning = False


class Api(Notifier):

    def __init__(self, user_key, api_token):
        self.user_key = user_key
        self.api_token = api_token
        self.client = DummyApi(Logger().logger)
        if self.is_valid_user_key(user_key) and self.is_valid_api_token(api_token):
            self.client = Client(user_key, api_token=api_token)

    def is_valid_user_key(self, user_key):
        return user_key != "user_key"

    def is_valid_api_token(self, api_token):
        return api_token != "api_token"

    @property
    def api(self):
        return self.client

    def send_message(self, message, title=None):
        self.api.send_message(message, title=title)

