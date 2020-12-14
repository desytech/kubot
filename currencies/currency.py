class Currency(object):
    def __init__(self, config):
        self.__currency = config['currency']

    @property
    def name(self):
        return self.__currency
