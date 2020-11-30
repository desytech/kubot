# Kubot
Lendbot for Kucoin with Pushover Support

![Kubot](https://github.com/desy83/kubot/workflows/Kubot/badge.svg)

# Preparation
- copy `config/config.demo` to `config/config`
- disable minimum_rate to enable automatic lending mode
- enter kucoin api key, api secret and passphrase
- enter pushover user_key and api_token (optional)

# Makefile
- `make` to list all makefile targets

# Build
- `cd kubot`
- `make build` or `docker build --tag kubot:0.1 .`

# Start
- `cd kubot`
- `make run-d` or ``docker run -v `pwd`/config/config:/app/config/config -d --name kubot kubot:0.1``
