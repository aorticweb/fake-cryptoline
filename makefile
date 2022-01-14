PY_RUN_CMD := docker-compose run mirror

format: format-py

format-py:
	$(PY_RUN_CMD) isort --atomic --apply
	$(PY_RUN_CMD) black --line-length 100 .

lint: ## Run flake8
	$(PY_RUN_CMD) flake8 --max-line-length 100 bot db mgmt
	# $(PY_RUN_CMD) mypy bot db mgmt

migrate:
	docker-compose up -d postgres
	$(PY_RUN_CMD) postgres-wait alembic upgrade head

create-migration:
	docker-compose up -d postgres
	$(PY_RUN_CMD) postgres-wait alembic upgrade head
	$(PY_RUN_CMD) alembic revision --autogenerate -m "$(MIGRATE_MSG)"

up:
	make migrate
	docker-compose up -d