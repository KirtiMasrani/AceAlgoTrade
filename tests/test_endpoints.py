import os
import subprocess
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]));
from app.api_client import call_api, DB_PATH


def setup_module(module):
    subprocess.run(["python", "scripts/populate_db.py"], check=True)


def teardown_module(module):
    if DB_PATH.exists():
        os.remove(DB_PATH)


def test_truedata_documented_endpoint():
    assert call_api("TrueData", "/marketdata", "GET") == {"status": "ok"}


def test_truedata_undocumented_endpoint():
    with pytest.raises(ValueError):
        call_api("TrueData", "/unknown", "GET")


def test_fyers_documented_endpoint():
    assert call_api("Fyers", "/quotes", "GET") == {"status": "ok"}


def test_fyers_undocumented_endpoint():
    with pytest.raises(ValueError):
        call_api("Fyers", "/unknown", "GET")
