import pytest
from config.config import Config
from notification.pushovernotifier import PushoverNotifier
from notification.slacknotifier import SlackNotifier

# Test Pushover Notifier

def set_pushover_config(user_key, api_token):
    config = Config()
    config.config.set('pushover', 'user_key', user_key)
    config.config.set('pushover', 'api_token', api_token)
    return config

@pytest.mark.parametrize("config, expected, desc", [
    (set_pushover_config('', ''), False, "empty key and token"),
    (set_pushover_config("user_key", "api_token"), False, "default key and token"),
    (set_pushover_config("invalidkey", "api_token"), False, "invalid key and empty token"),
    (set_pushover_config("user_key", "invalidtoken"), False, "invalid token and empty key"),
    (set_pushover_config("invalidkey", "invalidtoken"), False, "invalid key and token"),
    (set_pushover_config("uQIrZPO4dxGHdMR9qZZFQu27123456", "azGDOrEpk8GmAc0qoyamYeeU123456"), True, "valid key and token"),
    (set_pushover_config("uQIrZPO4dxGHdMR9qZZFQu27123456", "invalidtoken"), False, "valid key BUT invalid token"),
    (set_pushover_config("invalidkey", "azGDOrEpk8GmAc0qoyamYeeU123456"), False, "valid token BUT invalid key"),
])
def test_pushover_valid_config(config, expected, desc):
    assert PushoverNotifier.is_valid_config(config) == expected, desc

# Test Slack Notifier

def set_slack_config(api_token):
    config = Config()
    config.config.set('slack', 'api_token', api_token)
    return config

@pytest.mark.parametrize("config, expected, desc", [
    (set_slack_config(""), False, "empty token"),
    (set_slack_config("api_token"), False, "default token"),
    (set_slack_config("xoxb-1234567890123-1234567890123-123456789012345678901234"), True, "valid token"),
    (set_slack_config("xoxb-1234567890123456789012345678901234"), False, "invalid token"),
])
def test_slack_notifier(config, expected, desc):
    assert SlackNotifier.is_valid_config(config) == expected, desc

