
image := kubot
version := 2.0

build: ## build kubot docker image
	docker build --tag ${image}:${version} .
	docker image prune -f

compose: build ## compose and start kubot suite
	KUBOT_IMAGE=${image} KUBOT_VERSION=${version} docker-compose up -d

development: ## start kubot database and gui
	KUBOT_IMAGE=${image} KUBOT_VERSION=${version} docker-compose up -d postgres grafana

run-d: ## run kubot docker image detached
	docker stop kubot || true
	docker rm kubot || true
	docker run -d -v `pwd`/config/config:/app/config/config --name kubot ${image}:${version}

run: ## run kubot docker image attached
	docker run -v `pwd`/config/config:/app/config/config --name kubot ${image}:${version}

venv: ## bootstrap python3 venv
	@test -d "venv" || python3 -m venv venv

install: venv ## install kubot dependencies
	@source venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt;

test: venv ## run pytest suite
	@source venv/bin/activate; PYTHONPATH=`pwd` pytest


.PHONY: build run run-d venv development compose test install
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

