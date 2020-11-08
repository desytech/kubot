import os
from configparser import ConfigParser, ExtendedInterpolation


def property_wrapper(func):
    def function_wrapper(x):
        try:
            return func(x)
        except Exception as e:
            print("Error reading configuration:", e)
            exit(2)
    return function_wrapper


class Config(object):
    def __init__(self):
        self.__config = ConfigParser(interpolation=ExtendedInterpolation())
        self.__config.read(os.path.join(os.path.dirname(__file__), 'config'))

    @property
    @property_wrapper
    def api_key(self):
        return self.__config['api']['api_key']

    @property
    @property_wrapper
    def api_secret(self):
        return self.__config['api']['api_secret']

    @property
    @property_wrapper
    def api_passphrase(self):
        return self.__config['api']['api_passphrase']

    @property
    @property_wrapper
    def correction(self):
        return self.__config['bot'].getfloat('correction')

    @property
    @property_wrapper
    def default_interest(self):
        return self.__config['bot'].getfloat('default_interest')

    @property
    @property_wrapper
    def minimum_rate(self):
        return self.__config['bot'].getfloat('minimum_rate')

    @property
    @property_wrapper
    def charge(self):
        return self.__config['bot'].getfloat('charge')

    @property
    @property_wrapper
    def interval(self):
        return self.__config['bot'].getint('interval')

    @property
    @property_wrapper
    def pushover_enable(self):
        return self.__config['pushover']['enable']

    @property
    @property_wrapper
    def user_key(self):
        return self.__config['pushover']['user_key']

    @property
    @property_wrapper
    def api_token(self):
        return self.__config['pushover']['api_token']

config = Config()
