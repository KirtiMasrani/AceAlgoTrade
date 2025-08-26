INSERT INTO providers (name) VALUES ('DemoProvider');
INSERT INTO brokers (name) VALUES ('DemoBroker');
INSERT INTO users (username, email) VALUES ('testuser', 'test@example.com');
INSERT INTO symbols (ticker, name) VALUES ('AAPL', 'Apple Inc.'), ('GOOG', 'Alphabet Inc.');
INSERT INTO accounts (user_id, broker_id, provider_id, account_number) VALUES (1, 1, 1, 'ACC123');
INSERT INTO provider_endpoints (provider_id, name, url) VALUES (1, 'trade', 'https://api.demoprovider.com/trade');
INSERT INTO symbol_mappings (provider_id, symbol_id, provider_symbol) VALUES (1, 1, 'AAPL'), (1, 2, 'GOOG');
