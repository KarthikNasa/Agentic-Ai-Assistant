import sqlite3

import pytest


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    database_file = tmp_path / "test.db"

    monkeypatch.setenv(
        "DATABASE_PATH",
        str(database_file),
    )

    import importlib

    import agentic_ai.config
    import agentic_ai.storage.database

    agentic_ai.config.DATABASE_PATH = str(
        database_file
    )

    importlib.reload(
        agentic_ai.storage.database
    )

    db = agentic_ai.storage.database

    db.init_database()

    yield db


def test_database_initialization(test_database):
    connection = test_database.get_connection()

    try:
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """
        ).fetchall()

        names = {
            row["name"]
            for row in tables
        }

        assert "notes" in names
        assert "reminders" in names

    finally:
        connection.close()
