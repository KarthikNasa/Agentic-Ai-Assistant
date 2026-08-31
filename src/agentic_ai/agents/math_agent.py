from agentic_ai.llm import generate_text
from agentic_ai.tools.calculator import calculate


MATH_SYSTEM_PROMPT = """
You are the math specialist.

Solve the user's mathematical request accurately.

When the user gives a direct numerical expression,
use the calculator result provided to you.

Explain the result clearly and briefly.
"""


def run_math_agent(user_message: str) -> str:
    """
    Let Gemini understand the mathematical request,
    then calculate expressions when possible.
    """

    prompt = f"""
User request:

{user_message}

If this contains a straightforward mathematical expression,
identify it in this format:

EXPRESSION: <expression>

Otherwise explain the mathematical problem normally.
"""

    response = generate_text(
        prompt,
        system_instruction=MATH_SYSTEM_PROMPT,
    )

    if "EXPRESSION:" not in response:
        return response

    expression = response.split(
        "EXPRESSION:",
        1,
    )[1].strip().splitlines()[0].strip()

    try:
        result = calculate(expression)
    except ValueError:
        return response

    return generate_text(
        f"""
User request:
{user_message}

Calculated result:
{result}

Provide the final answer with a short explanation.
""",
        system_instruction=MATH_SYSTEM_PROMPT,
    )
