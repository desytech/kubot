# Kubot
Lendbot for Kucoin with Grafana Dashboard and Pushover Support

![Kubot](https://github.com/desy83/kubot/workflows/Kubot/badge.svg)

# Requirements
- Runtime: Make, Docker, Docker Compose
- Development: Python3

# Preparation
- copy `config/config.demo` to `config/config`
  
# Configuration

- **kucoin:  api_key, api_secret, api_passphrase**
- **correction**:
  - funding market variation limit
- **default_interest**:
  - default daily interest if funding market is empty
- **charge**:
  - charge orders with some additional amount
- **interval**:
  - kubot run interval in seconds
- **currencies**
  - currency specific settings
- *optional*: minimum_rate
  - unset: minimum lending limit would be disabled
- *optional*: pushover user_key, api_token
- *optional*: slack api_token, channel

# Makefile
- `make` to list all makefile targets

# Start
- Start Kubot Suite: `make compose`
- Open Dashboard: `http://localhost:3000`

# Stop
- Stop Kubot Suite: `make stop`

# Build
- Production: `make build`
- Development: `make build-dev`

# Developement
- `make venv`
- `make install`
- `make development`
- `source venv/bin/activate && python3 kubot.py`
  #### Database Connection
- `PGPASSWORD=kubot psql -h localhost -p 5433 -U kubot` 

# Test
- `make test`


# Notifiers
## Slack
1) Go to [slack apps](https://api.slack.com/apps) and create an app in a workspace you own.
2) Enter the `OAuth & Permission` page and add a scope with `chat:write` permissions to your app.
3) Create an api token and add into kubot config.

Per default the messages will be posted to the `#general` channel.
If you would like to post to a different channel add an existing channel name
to the config under `channel`.

## Pushover
1) Go to [pushover apps](https://pushover.net/) signup and purchase pushover one time payment.
2) Create Kubot application.
3) Add user key and created application token into kubot config.

