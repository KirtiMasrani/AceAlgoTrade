import sqlite3
from pathlib import Path

from parse_truedata_docs import parse_truedata_docs
from parse_fyers_docs import parse_fyers_docs

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "provider_endpoints.db"


def create_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS provider_endpoints (
            provider TEXT,
            endpoint_url TEXT,
            method TEXT,
            request_schema TEXT,
            response_schema TEXT,
            rate_limit TEXT,
            notes TEXT
        )
        """
    )


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    create_table(conn)
    conn.execute("DELETE FROM provider_endpoints")
    rows = parse_truedata_docs() + parse_fyers_docs()
    conn.executemany(
        """
        INSERT INTO provider_endpoints (
            provider, endpoint_url, method, request_schema, response_schema, rate_limit, notes
        ) VALUES (
            :provider, :endpoint_url, :method, :request_schema, :response_schema, :rate_limit, :notes
        )
        """,
        rows,
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
