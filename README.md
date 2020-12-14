# Kubot
Lendbot for Kucoin with Pushover Support

![Kubot](https://github.com/desy83/kubot/workflows/Kubot/badge.svg)

# Preparation
- copy `config/config.demo` to `config/config`
  
# Configuration
- **kucoin api_key, api_secret, api_passphrase**
- **correction**:
  - funding market variation limit
- **default_interest**:
  - default daily interest if funding market is empty
- **charge**:
  - charge orders with some additional amount
- **interval**:
  - kubot run interval in seconds
- *optional*: minimum_rate
  - unset: minimum lending limit would be disabled
- *optional* enter pushover user_key and api_token

# Makefile
- `make` to list all makefile targets

# Build
- `cd kubot`
- `make build`

# Start
- `cd kubot`
- `make run-d`

# Developement
- `cd kubot`
- `make venv`
- `make install`
- `source venv/bin/activate && python3 kubot.py`

# Test
- `cd kubot`
- `make test`