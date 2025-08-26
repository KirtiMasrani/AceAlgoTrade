# Fyers SDK

| Endpoint | Method | Request Schema | Response Schema | Rate Limit | Notes |
|---------|--------|----------------|-----------------|-----------|------|
| /quotes | GET | symbols: list | quotes: list | 100/min | Get quotes |
| /trade | POST | symbol: str, qty: int | trade_id: str | 60/min | Execute trade |
