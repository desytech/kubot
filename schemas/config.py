from schema import Schema, Or, And

currencies = Schema([
    {
        'currency': Or("USDT", "ETC"),
        'term': Or(7, 14, 28),
        'reserved_amount': And(int, lambda a: a >= 0)
    }
])
