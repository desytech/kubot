from schema import Schema, Or

currencies = Schema([
    {'currency': Or("USDT", "BTC", "EOS", "DASH")}
])
