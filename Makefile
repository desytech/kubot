.PHONY: build run run-d venv

image := kubot
version := 0.3

# check if python3 is installed
CHECK_PYTHON3 := $(shell type -P python3)
ifeq ('$(CHECK_PYTHON3)','')
    $(error package 'python3' not found)
endif

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
	@echo "make venv - bootstrap python3 venv"
venv:
	@test -d "venv" || python3 -m venv venv

help::
	@echo "make install - install kubot dependencies"
install: venv
	@source venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt;

help::
	@echo "make test - run pytest suite."
test: venv
	@source venv/bin/activate; PYTHONPATH=`pwd` pytest
