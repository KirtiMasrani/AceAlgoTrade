# TrueData SDK

| Endpoint | Method | Request Schema | Response Schema | Rate Limit | Notes |
|---------|--------|----------------|-----------------|-----------|------|
| /marketdata | GET | symbol: str | prices: list | 100/min | Fetch market data |
| /order | POST | symbol: str, qty: int | order_id: str | 50/min | Place order |
