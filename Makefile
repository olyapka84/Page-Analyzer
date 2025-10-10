install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

lint:
	uv run ruff check

build:
	./build.sh
render-start:
	@echo "Cleaning DATABASE_URL and ensuring sslmode=require..."
	# очистим переменную от мусора
	export DATABASE_URL_CLEAN=$$(printf %s "$$DATABASE_URL" | tr -d '\r\n' | sed -E 's/[[:space:]]+$$//'); \
	# добавим sslmode=require если нет
	case "$$DATABASE_URL_CLEAN" in \
	  *sslmode=*) : ;; \
	  *\?*) DATABASE_URL_CLEAN="$$DATABASE_URL_CLEAN&sslmode=require" ;; \
	  *)    DATABASE_URL_CLEAN="$$DATABASE_URL_CLEAN?sslmode=require" ;; \
	esac; \
	echo "Waiting for database..."; \
	for i in 1 2 3 4 5 6 7 8 9 10; do \
		psql "$$DATABASE_URL_CLEAN" -tAc "select 1" >/dev/null 2>&1 && break; \
		echo "DB not ready, retry $$i"; sleep 2; \
	done; \
	echo "Initializing schema if needed..."; \
	psql "$$DATABASE_URL_CLEAN" -tAc "select to_regclass('public.urls')" | grep -q urls \
		&& echo "Schema exists, skipping database.sql" \
		|| psql "$$DATABASE_URL_CLEAN" -v ON_ERROR_STOP=1 -f database.sql; \
	echo "Starting Gunicorn..."; \
	exec gunicorn -w 2 -b 0.0.0.0:$$PORT page_analyzer:app

PORT ?= 8000

start:
	uv run gunicorn -w 3 -b 0.0.0.0:$(PORT) page_analyzer:app
