install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

lint:
	uv run ruff check

build:
	./build.sh

render-start:
	bash -lc '\
		export DATABASE_URL_CLEAN="$$(printf %s "$$DATABASE_URL" | tr -d "\r\n" | sed -E "s/[[:space:]]+$$//")"; \
		case "$$DATABASE_URL_CLEAN" in \
		  *sslmode=*) : ;; \
		  *\?*) export DATABASE_URL_CLEAN="$$DATABASE_URL_CLEAN&sslmode=require" ;; \
		  *)    export DATABASE_URL_CLEAN="$$DATABASE_URL_CLEAN?sslmode=require" ;; \
		esac; \
		for i in {1..5}; do \
			psql "$$DATABASE_URL_CLEAN" -tAc "select 1" && break; \
			echo "DB not ready, retry $$i"; sleep 2; \
		done || exit 1; \
		psql "$$DATABASE_URL_CLEAN" -tAc "select to_regclass($$public.urls$$)" | grep -q urls \
			&& echo "Schema exists, skipping database.sql" \
			|| psql "$$DATABASE_URL_CLEAN" -v ON_ERROR_STOP=1 -f database.sql; \
		exec gunicorn -w 3 -b 0.0.0.0:$(PORT) page_analyzer:app \
	'

PORT ?= 8000

start:
	uv run gunicorn -w 3 -b 0.0.0.0:$(PORT) page_analyzer:app
