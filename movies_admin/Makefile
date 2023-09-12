help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'

#-----------------------------------------------------------------------------
dotenv: ## Create .env file from template .env.example file
	@test ! -f ./config/envs/.env && cp ./config/envs/.env.example ./config/envs/.env
	@echo ".env file created succesfully. Don't forget to change credentials in it!"

install: dotenv ## Create virtual env and install dependencies via poetry
	@poetry install --no-root

start-dev-server: ## start django dev server
	@poetry run python3 manage.py runserver

migrate: ## apply django migrations
	@poetry run python3 manage.py migrate --fake movies 0001
	@poetry run python3 manage.py migrate

makemigrations: ## create new migrations if required
	@poetry run python3 manage.py makemigrations

createsuperuser: ## create django superuser
	@poetry run python3 manage.py createsuperuser

createsuperuser-dev: ## autocreate test superuser with predefined login/pass
	@DJANGO_SUPERUSER_USERNAME=admin \
	DJANGO_SUPERUSER_PASSWORD=wow-so-secret \
	DJANGO_SUPERUSER_EMAIL=mail@mail.kek \
	poetry run python3 manage.py createsuperuser --noinput || true && \
	echo "Test Django superuser login/pass: admin / wow-so-secret"

translation: ## prepare files for translation
	@poetry run django-admin makemessages -i "venv" -i ".venv" -l en -l ru

compile-translation: ## compile translation
	@poetry run django-admin compilemessages -i "venv" -i ".venv" -l en -l ru


#-----------------------------------------------------------------------------
.PHONY: \
	dotenv \
	install \
	start-dev-server \
	migrate \
	makemigrations \
	createsuperuser \
	createsuperuser-dev \
	translation \
	compile-translation \
