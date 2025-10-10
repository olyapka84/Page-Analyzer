install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

lint:
	uv run ruff check

build:
	./build.sh

render-start:
	bash -lc 'for i in {1..15}; do psql "$$DATABASE_URL" -tAc "select 1" && exit 0; echo "DB not ready, retry $$i"; sleep 2; done; exit 1'

	psql "$$DATABASE_URL" -tAc "select to_regclass($$public.urls$$)" | grep -q urls \
		&& echo "Schema exists, skipping database.sql" \
		|| psql "$$DATABASE_URL" -v ON_ERROR_STOP=1 -f database.sql

	gunicorn -w 3 -b 0.0.0.0:$(PORT) page_analyzer:app


PORT ?= 8000

start:
	uv run gunicorn -w 3 -b 0.0.0.0:$(PORT) page_analyzer:app
