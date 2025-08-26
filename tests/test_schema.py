from pathlib import Path
import sqlite3
import pytest

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / 'db' / 'migrations' / '001_create_tables.sql'
SEED = ROOT / 'db' / 'seed.sql'


def run_script(cursor, path):
    with open(path, 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())


def test_tables_created():
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON')
    cur = conn.cursor()
    run_script(cur, MIGRATIONS)
    tables = {row[0] for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    expected = {
        'users', 'brokers', 'providers', 'accounts', 'symbols',
        'symbol_mappings', 'orders', 'trades', 'positions', 'provider_endpoints'
    }
    assert expected.issubset(tables)
    conn.close()


def test_relationships_and_constraints():
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON')
    cur = conn.cursor()
    run_script(cur, MIGRATIONS)

    cur.execute("INSERT INTO providers (name) VALUES ('P')")
    cur.execute("INSERT INTO brokers (name) VALUES ('B')")
    cur.execute("INSERT INTO users (username, email) VALUES ('u', 'u@example.com')")
    cur.execute("INSERT INTO symbols (ticker, name) VALUES ('SYM', 'Sym')")
    cur.execute("INSERT INTO accounts (user_id, broker_id, provider_id, account_number) VALUES (1,1,1,'ACC')")

    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO accounts (user_id, broker_id, provider_id, account_number) VALUES (2,1,1,'ACC2')")

    cur.execute("INSERT INTO symbol_mappings (provider_id, symbol_id, provider_symbol) VALUES (1,1,'SYM')")
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO symbol_mappings (provider_id, symbol_id, provider_symbol) VALUES (1,1,'SYM')")

    cur.execute("INSERT INTO positions (account_id, symbol_id, quantity, avg_price) VALUES (1,1,10,150)")
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO positions (account_id, symbol_id, quantity, avg_price) VALUES (1,1,20,155)")

    cur.execute("INSERT INTO provider_endpoints (provider_id, name, url) VALUES (1, 'trade', 'u')")
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO provider_endpoints (provider_id, name, url) VALUES (1, 'trade', 'u2')")

    cur.execute("INSERT INTO orders (account_id, symbol_id, side, quantity, price, status) VALUES (1,1,'BUY',10,100,'open')")
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO orders (account_id, symbol_id, side, quantity, price, status) VALUES (2,1,'BUY',10,100,'open')")

    cur.execute("INSERT INTO trades (order_id, account_id, symbol_id, quantity, price) VALUES (1,1,1,10,100)")
    with pytest.raises(sqlite3.IntegrityError):
        cur.execute("INSERT INTO trades (order_id, account_id, symbol_id, quantity, price) VALUES (2,1,1,10,100)")

    conn.close()


def test_seed_script():
    conn = sqlite3.connect(':memory:')
    conn.execute('PRAGMA foreign_keys = ON')
    cur = conn.cursor()
    run_script(cur, MIGRATIONS)
    run_script(cur, SEED)
    user = cur.execute('SELECT username FROM users').fetchone()[0]
    provider = cur.execute('SELECT name FROM providers').fetchone()[0]
    symbol_count = cur.execute('SELECT COUNT(*) FROM symbols').fetchone()[0]
    assert user == 'testuser'
    assert provider == 'DemoProvider'
    assert symbol_count == 2
    conn.close()

