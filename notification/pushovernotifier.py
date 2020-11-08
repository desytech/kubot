from notification.notify import Notifier
from pushover import Client

class Api(Notifier):

    def __init__(self, user_key, api_token):
        self.user_key = user_key
        self.api_token = api_token
        self.client = None

    @property
    def api(self):
        if self.client == None:
            self.client = Client(self.user_key, api_token=self.api_token)
        return self.client

    def send_message(self, message, title=None):
        self.api.send_message(message, title=title)

