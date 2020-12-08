import pytest
from helper import *


def test_convert_float_to_percentage_float():
    assert convert_float_to_percentage(0.00051) == '0.051%'

def test_convert_float_to_percentage_str():
    assert convert_float_to_percentage('0.00051') == '0.051%'

def test_convert_float_to_percentage_none():
    with pytest.raises(TypeError) as e:
        convert_float_to_percentage(None)
    assert e.type == TypeError
