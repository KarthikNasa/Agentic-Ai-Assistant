import json
import re

from agentic_ai.llm import generate_text


SYSTEM_PROMPT = """
You are the supervisor of a small personal AI assistant.

Available agents:

- math: mathematical calculations and arithmetic
- reminder: creating, listing, completing or deleting reminders
- notes: creating, listing, reading or deleting notes
- general: normal conversation and questions

Return ONLY valid JSON.

Format:
{
  "agent": "math|reminder|notes|general",
  "reason": "short reason"
}

Choose the most appropriate agent.
"""


def _extract_json(text: str) -> dict:
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL,
    )

    if match:
        return json.loads(match.group(0))

    raise ValueError(
        "Supervisor returned invalid JSON."
    )


def route_request(user_message: str) -> str:
    result = generate_text(
        user_message,
        system_instruction=SYSTEM_PROMPT,
    )

    data = _extract_json(result)

    agent = data.get("agent", "general")

    allowed = {
        "math",
        "reminder",
        "notes",
        "general",
    }

    if agent not in allowed:
        return "general"

    return agent
