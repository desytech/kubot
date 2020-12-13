class Currency(object):
    def __init__(self, config):
        self.__currency = config['currency']
        self.__term = config['term']

    @property
    def name(self):
        return self.__currency

    @property
    def term(self):
        return self.__term