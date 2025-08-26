import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "provider_endpoints.db"


def call_api(provider: str, endpoint: str, method: str):
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute(
            "SELECT 1 FROM provider_endpoints WHERE provider=? AND endpoint_url=? AND method=?",
            (provider, endpoint, method),
        )
        if cur.fetchone() is None:
            raise ValueError(f"Undocumented endpoint: {provider} {method} {endpoint}")
        return {"status": "ok"}
    finally:
        conn.close()
