import json
import re

from agentic_ai.llm import generate_text
from agentic_ai.tools.notes import (
    create_note,
    delete_note,
    get_note,
    list_notes,
)


SYSTEM_PROMPT = """
You are the notes specialist.

Convert the request into one of:

CREATE:
{
  "action": "create",
  "title": "...",
  "content": "..."
}

LIST:
{
  "action": "list"
}

GET:
{
  "action": "get",
  "id": 123
}

DELETE:
{
  "action": "delete",
  "id": 123
}

If information is missing:

{
  "action": "clarify",
  "message": "..."
}

Return ONLY JSON.
"""


def _parse_json(text: str) -> dict:
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL,
        )

        if not match:
            raise ValueError(
                "Invalid notes JSON."
            )

        return json.loads(match.group(0))


def run_notes_agent(
    user_message: str,
) -> str:

    result = generate_text(
        user_message,
        system_instruction=SYSTEM_PROMPT,
    )

    data = _parse_json(result)

    action = data.get("action")

    if action == "create":
        try:
            note = create_note(
                data["title"],
                data["content"],
            )

            return (
                f"Note created successfully.\n\n"
                f"**ID:** {note['id']}\n"
                f"**Title:** {note['title']}"
            )

        except (KeyError, ValueError) as exc:
            return f"Could not create note: {exc}"

    if action == "list":
        notes = list_notes()

        if not notes:
            return "You have no notes."

        lines = ["Your notes:"]

        for note in notes:
            lines.append(
                f"- #{note['id']} — {note['title']}"
            )

        return "\n".join(lines)

    if action == "get":
        try:
            note = get_note(int(data["id"]))

            if not note:
                return "Note not found."

            return (
                f"### {note['title']}\n\n"
                f"{note['content']}"
            )

        except (KeyError, ValueError):
            return "Please provide a valid note ID."

    if action == "delete":
        try:
            note_id = int(data["id"])

            if delete_note(note_id):
                return f"Note #{note_id} deleted."

            return "Note not found."

        except (KeyError, ValueError):
            return "Please provide a valid note ID."

    return data.get(
        "message",
        "I need more information about the note.",
    )
