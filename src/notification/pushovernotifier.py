import re

import const
from notification.notify import Notifier
from pushover import Client
from logger import Logger

REGEX_PUSHOVER_KEYS = r'^\w{30,30}$'

class Api(Notifier):

    def __init__(self, config):
        self.user_key = config.user_key
        self.api_token = config.api_token
        self.client = Client(user_key, api_token=api_token)

    @staticmethod
    def is_valid_config(config):
        if not config.user_key or not config.api_token:
            return False
        if not re.match(REGEX_PUSHOVER_KEYS, config.user_key):
            return False
        if not re.match(REGEX_PUSHOVER_KEYS, config.api_token):
            return False
        return True

    @property
    def api(self):
        return self.client

    def send_message(self, message, title=None):
        try:
            self.api.send_message(message, title=title)
        except Exception as e:
            Logger().logger.error("Pushover send message error: %s", e)

