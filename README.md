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
- optional: slack api_token

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
Go to [slack apps](https://api.slack.com/apps) and create a app in a workspace you own.
After that go to the `OAuth&Permission` page and add a scope to your app.
Minimum is `chat:write` (so you can send messages right :)).
After that you can create a api token. The token starts with `xoxb`.
Use that and add it to the config.
Per default the messages will be posted to the `#general` channel.
If you would like to post to a different channel add the existing channel name
to the config under `channel`.

