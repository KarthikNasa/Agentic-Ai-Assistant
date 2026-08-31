import json
import re

from agentic_ai.llm import generate_text
from agentic_ai.tools.reminders import (
    complete_reminder,
    create_reminder,
    delete_reminder,
    list_reminders,
)


SYSTEM_PROMPT = """
You are the reminder specialist.

Convert user requests into one of these JSON actions:

CREATE:
{
  "action": "create",
  "text": "...",
  "when": "..."
}

LIST:
{
  "action": "list"
}

COMPLETE:
{
  "action": "complete",
  "id": 123
}

DELETE:
{
  "action": "delete",
  "id": 123
}

If the request does not contain enough information,
return:

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
                "Invalid reminder JSON."
            )

        return json.loads(match.group(0))


def run_reminder_agent(
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
            reminder = create_reminder(
                data["text"],
                data["when"],
            )

            return (
                f"Reminder created successfully.\n\n"
                f"**ID:** {reminder['id']}\n"
                f"**Text:** {reminder['text']}\n"
                f"**Time:** {reminder['remind_at']}"
            )

        except (KeyError, ValueError) as exc:
            return f"Could not create reminder: {exc}"

    if action == "list":
        reminders = list_reminders()

        if not reminders:
            return "You have no active reminders."

        lines = ["Your active reminders:"]

        for reminder in reminders:
            lines.append(
                f"- #{reminder['id']} — "
                f"{reminder['text']} — "
                f"{reminder['remind_at']}"
            )

        return "\n".join(lines)

    if action == "complete":
        try:
            reminder_id = int(data["id"])
            success = complete_reminder(
                reminder_id
            )

            if success:
                return (
                    f"Reminder #{reminder_id} "
                    "marked as completed."
                )

            return (
                f"Reminder #{reminder_id} "
                "was not found."
            )

        except (KeyError, ValueError):
            return "Please provide a valid reminder ID."

    if action == "delete":
        try:
            reminder_id = int(data["id"])
            success = delete_reminder(
                reminder_id
            )

            if success:
                return (
                    f"Reminder #{reminder_id} deleted."
                )

            return (
                f"Reminder #{reminder_id} "
                "was not found."
            )

        except (KeyError, ValueError):
            return "Please provide a valid reminder ID."

    return data.get(
        "message",
        "I need more information about the reminder.",
    )
