from collections import namedtuple

Coin = namedtuple("Coin", [
    "symbol",
    "precision",
    "description"
])

USDT = Coin("USDT", 1,  "Tether")
TRX = Coin("TRX",   10, "Tron")

def All():
    return __all__

__all__ = [
    USDT,
    TRX,
]

if __name__ == '__main__':
    print(USDT)
