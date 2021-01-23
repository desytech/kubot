import pytest
from collections import namedtuple
from notification.pushovernotifier import PushoverNotifier
from notification.pushovernotifier import ErrInvalidPushoverUserKey
from notification.pushovernotifier import ErrInvalidPushoverApiToken
from notification.slacknotifier import SlackNotifier
from notification.slacknotifier import ErrInvalidSlackApiToken
from unittest.mock import Mock
from unittest.mock import MagicMock


class PushoverConfig(object):
    def __init__(self, user_key, api_token):
        self.user_key = user_key
        self.api_token = api_token
    def __repr__(self):
        return f"{self.user_key}:{self.api_token}"
P = PushoverConfig

@pytest.mark.parametrize("tinput, expected, desc", [
    (P("", ""), ErrInvalidPushoverUserKey, "empty key and token"),
    (P("user_key", "api_token"), False, "default key and token"),
    (P("invalidkey", "api_token"), False, "invalid key and empty token"),
    (P("user_key", "invalidtoken"), False, "invalid token and empty key"),
    (P("invalidkey", "invalidtoken"), ErrInvalidPushoverUserKey, "invalid key and token"),
    (P("uQIrZPO4dxGHdMR9qZZFQu27123456", "azGDOrEpk8GmAc0qoyamYeeU123456"), True, "valid key and token"),
    (P("uQIrZPO4dxGHdMR9qZZFQu27123456", "invalidtoken"), ErrInvalidPushoverApiToken, "valid key BUT invalid token"),
    (P("invalidkey", "azGDOrEpk8GmAc0qoyamYeeU123456"), ErrInvalidPushoverUserKey, "valid token BUT invalid key"),
])
def test_pushover_valid_config(tinput, expected, desc):
    do_test_valid_config(PushoverNotifier.is_valid_config, tinput, expected)


class SlackConfig(object):
    def __init__(self, api_token):
        self.slack_api_token = api_token
    def __repr__(self):
        return f"{self.api_token}"
S = SlackConfig

@pytest.mark.parametrize("tinput, expected, desc", [
    (S(""), ErrInvalidSlackApiToken, "empty token"),
    (S("api_token"), False, "default token"),
    (S("xoxb-1234567890123-1234567890123-123456789012345678901234"), True, "valid token"),
    (S("xoxb-1234567890123456789012345678901234"), ErrInvalidSlackApiToken, "invalid token"),
])
def test_slack_notifier(tinput, expected, desc):
    do_test_valid_config(SlackNotifier.is_valid_config, tinput, expected)


def do_test_valid_config(testfn, tinput, expected):
    try:
        result = testfn(tinput)
    except Exception as e:
        assert type(e) == type(expected())
        return
    assert result == expected, f"{testfn!r}({tinput!r}) != {expected!r}; got {result!r}"

