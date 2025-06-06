from schema import Schema, Or, And
from .static import Modes

currencies = Schema([
    {
        'currency': Or("USDT", "USDC"),
        'term': Or(7, 14, 28),
        'reserved_amount': And(int, lambda a: a >= 0)
    }
])

symbols = Schema([
    Or("ETH-USDT", "ETH-BTC")
])

modes = Schema(
    Or(Modes.DUAL, Modes.LENDING)
)
