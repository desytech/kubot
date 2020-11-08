
image := kubot
version := 0.1

build:
	docker build --tag ${image}:${version} .


run-d:
	docker run -d -v `pwd`/config/config:/app/config/config --name kubot ${image}:${version}

run:
	docker run -v `pwd`/config/config:/app/config/config --name kubot ${image}:${version}

vpy:
	python3 -m venv vpy
