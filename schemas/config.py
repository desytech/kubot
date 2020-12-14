from schema import Schema, Or

currencies = Schema([
    {
        'currency': Or("USDT"),
        'term': Or(7, 14, 28)
    }
])
