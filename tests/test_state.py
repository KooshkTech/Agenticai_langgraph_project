"""Tests for the State TypedDict used in the LangGraph state graph."""
from typing import get_args

from src.langgraphagenticai.state.state import State
from langgraph.graph.message import add_messages


def test_state_has_messages_field():
    """State must declare a 'messages' field."""
    assert "messages" in State.__annotations__


def test_state_messages_uses_add_messages_reducer():
    """The messages field must use add_messages as its reducer annotation."""
    annotation = State.__annotations__["messages"]
    # Annotated[list, add_messages] — extract the type and metadata
    args = get_args(annotation)
    assert args[0] == list
    assert args[1] == add_messages
