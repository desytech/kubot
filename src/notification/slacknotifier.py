import re
import requests
from notification.notify import Notifier
from logger import Logger


REGEX_SLACK_API_TOKEN = r'^xoxb-\w{13,13}-\w{13,13}-\w{24,24}$'

class ErrInvalidSlackApiToken(Exception):
    pass

class SlackNotifier(Notifier):

    def __init__(self, config):
        self.channel = config.slack_channel
        self.api_token = config.slack_api_token
        self.url = "https://slack.com/api/chat.postMessage"
        self.session = requests.Session() 

    @staticmethod
    def is_valid_config(config):
        if config.slack_api_token == 'api_token':
            Logger().logger.warning(f"slack notifier are defaults: {config.slack_api_token}. ignoring...")
            return False
        if not re.match(REGEX_SLACK_API_TOKEN, config.slack_api_token):
            raise ErrInvalidSlackApiToken(f"{config.slack_api_token}")
        return True

    def send_message(self, message, title=None):
        data = [
            ('token', self.api_token),
            ('channel', self.channel),
            ('text', f"{title}: {message}")
        ]
        self.session.post(self.url, data=data)

