# Kubot
Lendbot for Kucoin with Pushover Support

https://github.com/desy83/kubot/workflows/Kubot/badge.svg

# Preparation
- copy `config/config.demo` to `config/config`
- enter kucoin api key, api secret and passphrase
- enter pushover user_key and api_token

# Build
- `docker build --tag kubot:0.1 .`

# Start
- `cd kubot`
- ``docker run -v `pwd`/config/config:/app/config/config -d --name kubot kubot:0.1``