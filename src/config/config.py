import os
import sys
import json
from configparser import ConfigParser, ExtendedInterpolation

import const
from schemas.config import currencies as currencies_schema, symbols as symbols_schema, modes as modes_schema, \
    category_currency as category_currency_schema
from schemas.static import Modes


def property_wrapper(default=None):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
                return default if response is None else response
            except Exception as e:
                print("Error reading configuration:", e)
                exit(2)
        return wrapped
    return inner_decorator


class Config(object):
    def __init__(self):
        self.__config = ConfigParser(interpolation=ExtendedInterpolation())
        config_file = 'config.demo' if 'pytest' in sys.modules else 'config'
        self.__config.read(os.path.join(os.path.dirname(__file__), '../../config', config_file))

    @property
    def config(self):
        return self.__config

    @property
    @property_wrapper()
    def api_key(self):
        return self.__config['api']['api_key']

    @property
    @property_wrapper()
    def api_secret(self):
        return self.__config['api']['api_secret']

    @property
    @property_wrapper()
    def api_passphrase(self):
        return self.__config['api']['api_passphrase']

    @property
    @property_wrapper()
    def correction(self):
        return self.__config['bot'].getfloat('correction')

    @property
    @property_wrapper()
    def default_interest(self):
        return self.__config['bot'].getfloat('default_interest')

    @property
    @property_wrapper(default=const.DEFAULT_MIN_RATE)
    def minimum_rate(self):
        return self.__config['bot'].getfloat('minimum_rate')

    @property
    @property_wrapper()
    def charge(self):
        return self.__config['bot'].getfloat('charge')

    @property
    @property_wrapper()
    def interval(self):
        return self.__config['bot'].getint('interval')

    @property
    @property_wrapper(default='')
    def user_key(self):
        return self.__config['pushover'].get('user_key')

    @property
    @property_wrapper(default='')
    def api_token(self):
        return self.__config['pushover'].get('api_token')

    @property
    @property_wrapper(default=[])
    def currencies(self):
        currencies = json.loads(self.__config['bot'].get('currencies'))
        return currencies_schema.validate(currencies)

    @property
    @property_wrapper(default='')
    def slack_api_token(self):
        return self.__config['slack'].get('api_token')

    @property
    @property_wrapper(default='general')
    def slack_channel(self):
        return self.__config['slack'].get('channel')

    @property
    @property_wrapper(default=Modes.LENDING)
    def mode(self):
        modes = Modes(self.__config['bot'].get('mode'))
        return modes_schema.validate(modes)

    @property
    @property_wrapper(default=[])
    def symbols(self):
        symbols = json.loads(self.__config['bot'].get('symbols'))
        return symbols_schema.validate(symbols)

    @property
    @property_wrapper(default=[])
    def category_currency(self):
        category_currency = json.loads(self.__config['bot'].get('category_currency'))
        return category_currency_schema.validate(category_currency)
''
config = Config()
