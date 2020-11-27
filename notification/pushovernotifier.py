import re

import const
from notification.notify import Notifier
from pushover import Client


class Api(Notifier):

    def __init__(self, user_key, api_token):
        self.user_key = user_key
        self.api_token = api_token
        self.client = Client(user_key, api_token=api_token)

    @staticmethod
    def is_valid_key(key):
        if not key:
            return False
        return re.match(const.REGEX_PUSHOVER_KEYS, key)

    @property
    def api(self):
        return self.client

    def send_message(self, message, title=None):
        self.api.send_message(message, title=title)

