from pathlib import Path
import sys

# Add the project's src directory to Python's import path.
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


import streamlit as st

from agentic_ai.graph import invoke
from agentic_ai.storage.database import init_database


st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="🤖",
    layout="wide",
)


init_database()


st.title("🤖 Agentic AI Assistant")

st.caption(
    "Gemini + LangGraph + SQLite — free/local architecture"
)


with st.sidebar:
    st.header("Capabilities")

    st.markdown(
        """
        - 🧮 Mathematics
        - ⏰ Reminders
        - 📝 Notes
        - 💬 General AI
        """
    )

    st.divider()

    st.markdown(
        """
        ### Example prompts

        **Math**

        `Calculate 125 * 48`

        **Reminder**

        `Remind me in 20 minutes to drink water`

        **Notes**

        `Save a note titled Project Ideas`

        **General**

        `Explain LangGraph simply`
        """
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input(
    "What can I help you with?"
)


if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = invoke(prompt)

            except Exception as exc:
                response = (
                    "I encountered an error:\n\n"
                    f"`{type(exc).__name__}: {exc}`"
                )

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
