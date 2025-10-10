# page_analyzer/database.py
import os
import time
import psycopg2
from urllib.parse import urlparse, unquote


def _parse_env_url() -> dict:
    raw = (os.getenv("DATABASE_URL") or "").replace("\r", "").replace("\n", "").strip()
    if not raw:
        raise RuntimeError("DATABASE_URL is empty")

    u = urlparse(raw)

    host = u.hostname
    port = u.port or 5432
    dbname = u.path.lstrip("/")
    user = unquote(u.username) if u.username else None
    password = unquote(u.password) if u.password else None

    if not (host and dbname and user and password):
        raise RuntimeError("Malformed DATABASE_URL (missing parts)")

    return {
        "host": host,
        "port": port,
        "dbname": dbname,
        "user": user,
        "password": password,
        "sslmode": "require",
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 3,
        "options": "-c statement_timeout=60000",
    }


def get_connection(retries: int = 5, delay: float = 0.5):
    params = _parse_env_url()
    last_err = None
    for _ in range(retries):
        try:
            return psycopg2.connect(**params)
        except psycopg2.OperationalError as e:
            last_err = e
            time.sleep(delay)
            delay = min(delay * 2, 5)
    raise last_err
