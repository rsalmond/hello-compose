SHELL=bash

NETWORK_EXISTS:=$(shell docker network ls -q -f name=hello)
OVERRIDE_EXISTS:=$(shell find . -maxdepth 1 -name docker-compose.override.yml)
HELLO_CONTAINER:=$(shell docker ps | grep "hello:latest" | awk -F " " '{print $$1}')

.DEFAULT_GOAL := up

up:
	docker-compose up

build:
	docker build -t hello:latest .

dev:
ifeq ($(OVERRIDE_EXISTS),)
	@echo "No override file found, copy the example or create one and try again."
	@echo "Eg. cp docker-compose.override.dev.yml docker-compose.override.yml"
	@/bin/false
endif
ifeq ($(HELLO_CONTAINER),)
	@echo "Hello container is not running, start it first with: make up"
else
	@echo "Dropping you into your app container. For an interactive app shell run: python manage.py shell"
	docker exec -it $(HELLO_CONTAINER) /bin/bash
endif

update-requirements:
	pip freeze | grep -v pkg-resources > ./hello/requirements.txt

testdata:
	curl --header "Content-Type: application/json" -X POST --data '{"name":"dude","adjective":"nice", "adverb": "really"}' http://localhost:5000/hello/v1/greetings/3

fromscratch: build setup up

test:
	docker run --env-file test.env hello:latest nosetests -s

setup: setup-network setup-db

setup-network:
ifeq ($(NETWORK_EXISTS),)
	docker network create hello
endif

setup-db:
	@echo "starting database container"
	docker-compose up -d master slave
	@# give it a moment to start up
	@sleep 15
	docker run --env-file setup.env --link master:master --network hello hello:latest python manage.py db_create
	@echo "stopping database container"
	docker-compose stop

nuke:
	docker-compose down
ifneq ($(NETWORK_EXISTS),)
	docker network rm hello
endif
	docker volume rm hellocompose_mysql-master-data
	docker volume rm hellocompose_mysql-slave-data

.PHONY: up build update-requirements upload-file fromscratch setup setup-network setup-db nuke dev
