from datetime import datetime, timedelta
import re

from agentic_ai.storage.database import (
    execute,
    fetch_all,
)


def _parse_time(text: str) -> datetime:
    """
    Parse simple natural-language reminder times.

    Supported:
        in 10 minutes
        in 2 hours
        in 3 days
        tomorrow 09:00
        tomorrow at 9:30
        today 18:00
    """

    value = text.strip().lower()

    now = datetime.now()

    relative = re.search(
        r"in\s+(\d+)\s+(minute|minutes|hour|hours|day|days)",
        value,
    )

    if relative:
        amount = int(relative.group(1))
        unit = relative.group(2)

        if "minute" in unit:
            return now + timedelta(minutes=amount)

        if "hour" in unit:
            return now + timedelta(hours=amount)

        if "day" in unit:
            return now + timedelta(days=amount)

    time_match = re.search(
        r"(today|tomorrow)(?:\s+at)?\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?",
        value,
    )

    if time_match:
        day_name = time_match.group(1)
        hour = int(time_match.group(2))
        minute = int(time_match.group(3) or 0)
        am_pm = time_match.group(4)

        if am_pm:
            if am_pm == "pm" and hour != 12:
                hour += 12

            if am_pm == "am" and hour == 12:
                hour = 0

        target_date = now.date()

        if day_name == "tomorrow":
            target_date += timedelta(days=1)

        result = datetime.combine(
            target_date,
            datetime.min.time(),
        ).replace(
            hour=hour,
            minute=minute,
        )

        if day_name == "today" and result <= now:
            raise ValueError(
                "That time has already passed today."
            )

        return result

    raise ValueError(
        "Could not understand reminder time. "
        "Try 'in 20 minutes' or 'tomorrow at 9:00'."
    )


def create_reminder(
    text: str,
    when: str,
) -> dict:
    text = text.strip()

    if not text:
        raise ValueError(
            "Reminder text cannot be empty."
        )

    remind_at = _parse_time(when)

    reminder_id = execute(
        """
        INSERT INTO reminders (text, remind_at)
        VALUES (?, ?)
        """,
        (
            text,
            remind_at.isoformat(timespec="minutes"),
        ),
    )

    return {
        "id": reminder_id,
        "text": text,
        "remind_at": remind_at.isoformat(
            timespec="minutes"
        ),
        "completed": False,
    }


def list_reminders(
    include_completed: bool = False,
) -> list[dict]:
    if include_completed:
        return fetch_all(
            """
            SELECT *
            FROM reminders
            ORDER BY remind_at ASC
            """
        )

    return fetch_all(
        """
        SELECT *
        FROM reminders
        WHERE completed = 0
        ORDER BY remind_at ASC
        """
    )


def complete_reminder(
    reminder_id: int,
) -> bool:
    result = execute(
        """
        UPDATE reminders
        SET completed = 1
        WHERE id = ?
        """,
        (reminder_id,),
    )

    return result > 0


def delete_reminder(
    reminder_id: int,
) -> bool:
    result = execute(
        """
        DELETE FROM reminders
        WHERE id = ?
        """,
        (reminder_id,),
    )

    return result > 0


def get_due_reminders() -> list[dict]:
    now = datetime.now().isoformat(
        timespec="minutes"
    )

    return fetch_all(
        """
        SELECT *
        FROM reminders
        WHERE completed = 0
          AND remind_at <= ?
        ORDER BY remind_at ASC
        """,
        (now,),
    )
