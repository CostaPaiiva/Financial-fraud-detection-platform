.PHONY: up down restart logs ps install test

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down
	docker compose up -d

logs:
	docker compose logs -f

ps:
	docker compose ps

install:
	pip install -r requirements.txt

test:
	pytest