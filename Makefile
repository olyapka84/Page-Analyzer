install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

lint:
	uv run ruff check

build:
	./build.sh

render-start:
	PGSSLMODE=require psql "$$DATABASE_URL" -tAc "SELECT to_regclass('public.urls');" | grep -q urls \
		&& echo 'Schema exists, skipping database.sql' \
		|| PGSSLMODE=require psql "$$DATABASE_URL" -v ON_ERROR_STOP=1 -f database.sql
	gunicorn -w 3 -b 0.0.0.0:$(PORT) page_analyzer:app

PORT ?= 8000

start:
	uv run gunicorn -w 3 -b 0.0.0.0:$(PORT) page_analyzer:app
