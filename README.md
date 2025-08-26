# AceAlgoTrade

This repository tracks API endpoints from different market data providers.

## Usage

1. Populate the SQLite database from bundled SDK docs:
   ```bash
   python scripts/populate_db.py
   ```
2. Use `app.api_client.call_api` to perform a documented call. Calls to
   undocumented endpoints raise an error.

## Tests

Run `pytest` to execute integration tests ensuring undocumented endpoints are rejected.
