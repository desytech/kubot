import os
import json
from configparser import ConfigParser, ExtendedInterpolation

import const
from schemas.config import currencies as currencies_schema


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
        self.__config.read(os.path.join(os.path.dirname(__file__), 'config'))

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
    @property_wrapper()
    def user_key(self):
        return self.__config['pushover'].get('user_key')

    @property
    @property_wrapper()
    def api_token(self):
        return self.__config['pushover'].get('api_token')

    @property
    @property_wrapper(default=[])
    def currencies(self):
        currencies = json.loads(self.__config['bot'].get('currencies'))
        return currencies_schema.validate(currencies)


config = Config()
