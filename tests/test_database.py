import pytest
from pykeepass.exceptions import CredentialsError

from keecli.database import KeePassDatabase


def test_open_db_with_correct_password(test_db_path):
    _ = KeePassDatabase(test_db_path, "test_password")
    assert True


def test_open_db_with_incorrect_password(test_db_path):
    with pytest.raises(CredentialsError):
        _ = KeePassDatabase(test_db_path, "test_incorrect_password")
