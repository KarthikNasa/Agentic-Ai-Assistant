from langchain_openai import ChatOpenAI

from .config import settings


def get_llm() -> ChatOpenAI:
    """Create the LLM used by the agents."""

    if not settings.openai_api_key:
        raise ValueError(
            "OPENAI_API_KEY is not configured. "
            "Create a .env file and add your API key."
        )

    return ChatOpenAI(
        model=settings.model_name,
        temperature=0,
        api_key=settings.openai_api_key,
    )
