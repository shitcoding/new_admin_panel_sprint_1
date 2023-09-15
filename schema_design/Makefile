help:  ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[0;32m%-30s\033[0m %s\n", $$1, $$2}'

#-----------------------------------------------------------------------------
start-postgres-docker: ## Start docker container with postgres
	docker run -d \
  -p 5432:5432 \
  -v ./postgres_data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=123qwe \
  -e POSTGRES_USER=app \
  -e POSTGRES_DB=movies_database  \
  postgres:13

create-schema: ## Create db schema on local postgres instance
	PGPASSWORD=123qwe psql -h 127.0.0.1 -U app -d movies_database -f ./movies_database.ddl

PHONY:
	start-postgres-docker \
	create-schema \
