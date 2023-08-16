from pathlib import Path

import pytest


@pytest.fixture
def test_db_path():
    yield Path(__file__).parent / "dbs" / "test_db.kdbx"
