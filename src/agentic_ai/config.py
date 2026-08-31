import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Gemini model with free-tier availability.
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.1-flash-lite",
)

DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    str(PROJECT_ROOT / "data" / "assistant.db"),
)

MAX_LLM_OUTPUT_TOKENS = int(
    os.getenv("MAX_LLM_OUTPUT_TOKENS", "1024")
)


def validate_config() -> None:
    """Validate application configuration."""

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Copy .env.example to .env and add your Gemini API key."
        )
