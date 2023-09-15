help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'


#-----------------------------------------------------------------------------
dotenv:  ## Create .env file from template .env.example file
	@test ! -f ./.env && cp ./.env.example ./.env
	@echo ".env file created succesfully. Don't forget to change credentials in it!"

install: dotenv ## Create virtual env and install dependencies via poetry
	@poetry install --no-root

sqlite_to_postgres: ## Run import of sqlite data to postgres
	@poetry run python3 load_data.py

test: ## run tests
	@export PYTHONPATH="${PYTHONPATH}:$(pwd)" && \
	poetry run pytest


#-----------------------------------------------------------------------------
.PHONY: \
	dotenv \
	install \
	sqlite_to_postgres \
	test \
