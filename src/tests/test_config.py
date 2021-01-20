from config.config import property_wrapper

default = 'foo'

@property_wrapper(default=default)
def decorator(value):
    return value

def test_property_decorator_default():
    assert decorator(None) == default

def test_property_decorator_value():
    value = 'bar'
    assert decorator(value) == value
