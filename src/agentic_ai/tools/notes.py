from agentic_ai.storage.database import (
    execute,
    fetch_all,
    fetch_one,
)


def create_note(
    title: str,
    content: str,
) -> dict:
    title = title.strip()
    content = content.strip()

    if not title:
        raise ValueError("Note title cannot be empty.")

    if not content:
        raise ValueError("Note content cannot be empty.")

    note_id = execute(
        """
        INSERT INTO notes (title, content)
        VALUES (?, ?)
        """,
        (title, content),
    )

    return {
        "id": note_id,
        "title": title,
        "content": content,
    }


def list_notes() -> list[dict]:
    return fetch_all(
        """
        SELECT
            id,
            title,
            content,
            created_at,
            updated_at
        FROM notes
        ORDER BY created_at DESC
        """
    )


def get_note(note_id: int) -> dict | None:
    return fetch_one(
        """
        SELECT
            id,
            title,
            content,
            created_at,
            updated_at
        FROM notes
        WHERE id = ?
        """,
        (note_id,),
    )


def delete_note(note_id: int) -> bool:
    result = execute(
        """
        DELETE FROM notes
        WHERE id = ?
        """,
        (note_id,),
    )

    return result > 0
