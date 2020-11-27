.PHONY: build run run-d venv

image := kubot
version := 0.1

help::
	@echo "make build - build kubot docker image."
build:
	docker build --tag ${image}:${version} .

help::
	@echo "make run-d - run kubot docker image detached."
run-d:
	docker run -d -v `pwd`/config/config:/app/config/config --name kubot ${image}:${version}

help::
	@echo "make run - run kubot docker image attached."
run:
	docker run -v `pwd`/config/config:/app/config/config --name kubot ${image}:${version}

help::
	@echo "make venv - bootstrap python3 venv."
venv:
	python3 -m venv venv
