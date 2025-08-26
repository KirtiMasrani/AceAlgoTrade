PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE brokers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE providers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE accounts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  broker_id INTEGER NOT NULL,
  provider_id INTEGER,
  account_number TEXT NOT NULL UNIQUE,
  FOREIGN KEY(user_id) REFERENCES users(id),
  FOREIGN KEY(broker_id) REFERENCES brokers(id),
  FOREIGN KEY(provider_id) REFERENCES providers(id)
);

CREATE TABLE symbols (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker TEXT NOT NULL UNIQUE,
  name TEXT
);

CREATE TABLE symbol_mappings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  provider_id INTEGER NOT NULL,
  symbol_id INTEGER NOT NULL,
  provider_symbol TEXT NOT NULL,
  FOREIGN KEY(provider_id) REFERENCES providers(id),
  FOREIGN KEY(symbol_id) REFERENCES symbols(id),
  UNIQUE(provider_id, provider_symbol),
  UNIQUE(provider_id, symbol_id)
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  symbol_id INTEGER NOT NULL,
  side TEXT NOT NULL,
  quantity REAL NOT NULL,
  price REAL,
  status TEXT NOT NULL,
  placed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(account_id) REFERENCES accounts(id),
  FOREIGN KEY(symbol_id) REFERENCES symbols(id)
);

CREATE TABLE trades (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  account_id INTEGER NOT NULL,
  symbol_id INTEGER NOT NULL,
  quantity REAL NOT NULL,
  price REAL NOT NULL,
  executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(order_id) REFERENCES orders(id),
  FOREIGN KEY(account_id) REFERENCES accounts(id),
  FOREIGN KEY(symbol_id) REFERENCES symbols(id)
);

CREATE TABLE positions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER NOT NULL,
  symbol_id INTEGER NOT NULL,
  quantity REAL NOT NULL,
  avg_price REAL NOT NULL,
  FOREIGN KEY(account_id) REFERENCES accounts(id),
  FOREIGN KEY(symbol_id) REFERENCES symbols(id),
  UNIQUE(account_id, symbol_id)
);

CREATE TABLE provider_endpoints (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  provider_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  url TEXT NOT NULL,
  FOREIGN KEY(provider_id) REFERENCES providers(id),
  UNIQUE(provider_id, name)
);
