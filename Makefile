.PHONY: build run run-d venv

image := kubot
version := 0.3

help::
	@echo "make build - build kubot docker image."
build:
	docker build --tag ${image}:${version} .
	docker image prune -f

help::
	@echo "make run-d - run kubot docker image detached."
run-d:
	docker stop kubot || true
	docker rm kubot || true
	docker run -d -v `pwd`/config/config:/app/config/config --name kubot ${image}:${version}

help::
	@echo "make run - run kubot docker image attached."
run:
	docker run -v `pwd`/config/config:/app/config/config --name kubot ${image}:${version}

help::
	@echo "make venv - bootstrap python3 venv."
venv:
	python3 -m venv venv

help::
	@echo "make test - run pytest suite."
test:
	PYTHONPATH=`pwd` pytest
