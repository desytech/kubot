import logging
from singleton import Singleton


class Logger(metaclass=Singleton):

    def __init__(self):
        logger = logging.getLogger('kubot')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.propagate = False
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        self.__logger = logger

    @property
    def logger(self):
        return self.__logger


