import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    database_path: str = os.getenv(
        "DATABASE_PATH",
        "agentic_assistant.db",
    )


settings = Settings()
