import os
import time
import psycopg2


def _normalize_dsn(url: str) -> str:
    url = (url or "").replace("\r", "").replace("\n", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is empty")
    if "sslmode=" not in url:
        url += ("&" if "?" in url else "?") + "sslmode=require"
    return url


def get_connection(retries: int = 5, delay: float = 0.5):
    dsn = _normalize_dsn(os.getenv("DATABASE_URL", ""))
    last_err = None
    for _ in range(retries):
        try:
            return psycopg2.connect(
                dsn,
                connect_timeout=10,
                keepalives=1,
                keepalives_idle=30,
                keepalives_interval=10,
                keepalives_count=3,
                options="-c statement_timeout=60000",
            )
        except psycopg2.OperationalError as e:
            last_err = e
            time.sleep(delay)
            delay *= 2
    raise last_err
