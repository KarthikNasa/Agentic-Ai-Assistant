from functools import lru_cache

from google import genai
from google.genai import types

from agentic_ai.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_LLM_OUTPUT_TOKENS,
)


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(
    prompt: str,
    system_instruction: str | None = None,
) -> str:
    """
    Generate text using Gemini.

    This function deliberately uses only the Gemini API.
    All application tools remain local and free.
    """

    client = get_client()

    config = types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=MAX_LLM_OUTPUT_TOKENS,
        system_instruction=system_instruction,
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text.strip()
