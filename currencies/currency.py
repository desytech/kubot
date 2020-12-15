class Currency(object):
    def __init__(self, config):
        self.__currency = config['currency']
        self.__term = config['term']
        self.__reserved_amount = config['reserved_amount']

    @property
    def name(self):
        return self.__currency

    @property
    def term(self):
        return self.__term

    @property
    def reserved_amount(self):
        return self.__reserved_amount