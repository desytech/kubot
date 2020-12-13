from schema import Schema, Or

currencies = Schema([
    {
        'currency': Or("USDT", "ETC"),
        'term': Or(7, 14, 28)
    }
])
