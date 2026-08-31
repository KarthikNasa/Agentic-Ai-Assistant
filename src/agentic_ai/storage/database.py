import sqlite3
from pathlib import Path
from typing import Any

from agentic_ai.config import DATABASE_PATH


def _ensure_directory() -> None:
    Path(DATABASE_PATH).parent.mkdir(
        parents=True,
        exist_ok=True,
    )


def get_connection() -> sqlite3.Connection:
    _ensure_directory()

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False,
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database() -> None:
    """Create application tables."""

    connection = get_connection()

    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                remind_at TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        connection.commit()

    finally:
        connection.close()


def execute(
    query: str,
    parameters: tuple[Any, ...] = (),
) -> int:
    """Execute INSERT/UPDATE/DELETE."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            query,
            parameters,
        )

        connection.commit()

        return cursor.lastrowid or cursor.rowcount

    finally:
        connection.close()


def fetch_all(
    query: str,
    parameters: tuple[Any, ...] = (),
) -> list[dict[str, Any]]:
    """Execute SELECT and return dictionaries."""

    connection = get_connection()

    try:
        rows = connection.execute(
            query,
            parameters,
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()


def fetch_one(
    query: str,
    parameters: tuple[Any, ...] = (),
) -> dict[str, Any] | None:
    """Execute SELECT and return one dictionary."""

    connection = get_connection()

    try:
        row = connection.execute(
            query,
            parameters,
        ).fetchone()

        return dict(row) if row else None

    finally:
        connection.close()
