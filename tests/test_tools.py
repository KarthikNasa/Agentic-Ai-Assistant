def test_notes_crud(tmp_path, monkeypatch):
    import agentic_ai.config

    database_file = tmp_path / "notes.db"

    monkeypatch.setattr(
        agentic_ai.config,
        "DATABASE_PATH",
        str(database_file),
    )

    from agentic_ai.storage import database

    database.init_database()

    from agentic_ai.tools.notes import (
        create_note,
        delete_note,
        get_note,
        list_notes,
    )

    note = create_note(
        "Test",
        "Hello world",
    )

    assert note["title"] == "Test"

    fetched = get_note(
        note["id"]
    )

    assert fetched is not None
    assert fetched["content"] == "Hello world"

    notes = list_notes()

    assert len(notes) == 1

    assert delete_note(
        note["id"]
    )

    assert get_note(
        note["id"]
    ) is None


def test_reminder_creation(tmp_path, monkeypatch):
    import agentic_ai.config

    database_file = tmp_path / "reminders.db"

    monkeypatch.setattr(
        agentic_ai.config,
        "DATABASE_PATH",
        str(database_file),
    )

    from agentic_ai.storage import database

    database.init_database()

    from agentic_ai.tools.reminders import (
        create_reminder,
        list_reminders,
    )

    reminder = create_reminder(
        "Test reminder",
        "in 10 minutes",
    )

    assert reminder["text"] == "Test reminder"

    reminders = list_reminders()

    assert len(reminders) == 1
