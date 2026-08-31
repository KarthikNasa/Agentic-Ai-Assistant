from typing import TypedDict

from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from agentic_ai.agents.math_agent import (
    run_math_agent,
)
from agentic_ai.agents.notes_agent import (
    run_notes_agent,
)
from agentic_ai.agents.reminder_agent import (
    run_reminder_agent,
)
from agentic_ai.agents.supervisor import (
    route_request,
)
from agentic_ai.llm import generate_text
from agentic_ai.storage.database import (
    init_database,
)


class AssistantState(TypedDict, total=False):
    user_message: str
    agent: str
    response: str


def supervisor_node(
    state: AssistantState,
) -> AssistantState:

    agent = route_request(
        state["user_message"]
    )

    return {
        **state,
        "agent": agent,
    }


def math_node(
    state: AssistantState,
) -> AssistantState:

    return {
        **state,
        "response": run_math_agent(
            state["user_message"]
        ),
    }


def reminder_node(
    state: AssistantState,
) -> AssistantState:

    return {
        **state,
        "response": run_reminder_agent(
            state["user_message"]
        ),
    }


def notes_node(
    state: AssistantState,
) -> AssistantState:

    return {
        **state,
        "response": run_notes_agent(
            state["user_message"]
        ),
    }


def general_node(
    state: AssistantState,
) -> AssistantState:

    response = generate_text(
        state["user_message"],
        system_instruction="""
You are a helpful personal AI assistant.

Answer naturally and concisely.

You do not have access to external paid services.
The application provides separate tools for:
- mathematics
- reminders
- notes
""",
    )

    return {
        **state,
        "response": response,
    }


def route_after_supervisor(
    state: AssistantState,
) -> str:

    return state.get(
        "agent",
        "general",
    )


def build_graph():
    init_database()

    builder = StateGraph(
        AssistantState
    )

    builder.add_node(
        "supervisor",
        supervisor_node,
    )

    builder.add_node(
        "math",
        math_node,
    )

    builder.add_node(
        "reminder",
        reminder_node,
    )

    builder.add_node(
        "notes",
        notes_node,
    )

    builder.add_node(
        "general",
        general_node,
    )

    builder.add_edge(
        START,
        "supervisor",
    )

    builder.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "math": "math",
            "reminder": "reminder",
            "notes": "notes",
            "general": "general",
        },
    )

    builder.add_edge(
        "math",
        END,
    )

    builder.add_edge(
        "reminder",
        END,
    )

    builder.add_edge(
        "notes",
        END,
    )

    builder.add_edge(
        "general",
        END,
    )

    return builder.compile()


graph = build_graph()


def invoke(
    user_message: str,
) -> str:

    result = graph.invoke(
        {
            "user_message": user_message,
        }
    )

    return result["response"]

