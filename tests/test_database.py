"""
    Database interface unit tests
"""

import pytest

from nameko_mongoengine.database import Database


@pytest.fixture
def database(mocker):
    mocker.patch('nameko_mongoengine.database.get_db', side_effect={"default": "default_conn", "test": "test_conn"}.get)
    return Database


def test_create(database):
    engine = database("default")
    assert engine._alias == "default"
    assert engine.db == "default_conn"

    # Test temporary change in alias
    assert engine.with_alias("test").db == "test_conn"
    assert engine.db == "default_conn"

    # Test unknown alias
    assert engine.with_alias("others").db is None
