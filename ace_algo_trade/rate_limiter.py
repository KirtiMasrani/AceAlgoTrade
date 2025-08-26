import sqlite3
import time
from threading import Lock
from typing import Optional


class RateLimiter:
    """Persist rate limit metadata and enforce client-side throttling."""

    def __init__(self, db_path: str = "rate_limits.db") -> None:
        self.db_path = db_path
        self._lock = Lock()
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS limits (
                    provider TEXT PRIMARY KEY,
                    request_limit INTEGER NOT NULL,
                    window INTEGER NOT NULL,
                    count INTEGER NOT NULL,
                    last_reset REAL NOT NULL
                )
                """
            )
            conn.commit()

    def configure(self, provider: str, limit: int, window: int) -> None:
        """Set the rate limit information for a provider."""
        now = time.time()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO limits(provider, request_limit, window, count, last_reset)
                VALUES(?, ?, ?, ?, ?)
                """,
                (provider, limit, window, 0, now),
            )
            conn.commit()

    def throttle(self, provider: str) -> None:
        """Block if the provider's rate limit would be exceeded."""
        with self._lock, sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT request_limit, window, count, last_reset FROM limits WHERE provider=?",
                (provider,),
            ).fetchone()
            if not row:
                return
            limit, window, count, last_reset = row
            now = time.time()
            if now - last_reset >= window:
                count = 0
                last_reset = now
            if count >= limit:
                sleep_time = window - (now - last_reset)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                count = 0
                last_reset = time.time()
            conn.execute(
                "UPDATE limits SET count=?, last_reset=? WHERE provider=?",
                (count + 1, last_reset, provider),
            )
            conn.commit()
