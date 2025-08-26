# AceAlgoTrade

Utilities for building trading algorithms with robust API access.

## Modules

- `ace_algo_trade/auth.py`: token acquisition and refresh via `TokenManager`.
- `ace_algo_trade/rest_client.py`: retry/backoff HTTP requests with optional rate limiting.
- `ace_algo_trade/websocket_client.py`: WebSocket client with reconnection and heartbeat.
- `ace_algo_trade/rate_limiter.py`: persists rate limit metadata and enforces throttling.
