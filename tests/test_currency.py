import pytest
from currencies.currency import Currency

@pytest.fixture
def currency():
    return Currency({"currency": "USDT", "term": 28, "reserved_amount": 10})

def test_get_currency_name(currency):
    assert currency.name == 'USDT'

def test_get_currency_term(currency):
    assert currency.term == 28

def test_get_currency_reserved_amount(currency):
    assert currency.reserved_amount == 10