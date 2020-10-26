# Kubot
Lendbot for Kucoin

# Preparation
- copy `config/config.demo` to `config/config`
- enter api key, api secret and passphrase

# Build
- `docker build --tag kubot:0.1 .`

# Start

- `docker run -d --name kubot kubot:0.1`