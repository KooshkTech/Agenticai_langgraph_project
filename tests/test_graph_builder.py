"""Tests for the GraphBuilder class."""
from unittest.mock import MagicMock, patch

from src.langgraphagenticai.graph.graph_builder import GraphBuilder


class MockLLM:
    """Minimal mock LLM for graph construction tests."""

    def __init__(self):
        self.bound_tools = None

    def invoke(self, messages):
        return "mock response"

    def bind_tools(self, tools):
        self.bound_tools = tools
        return self


def test_setup_graph_basic_chatbot():
    """setup_graph('Basic Chatbot') must return a compiled graph with a 'chatbot' node."""
    mock_llm = MockLLM()
    builder = GraphBuilder(mock_llm)
    graph = builder.setup_graph("Basic Chatbot")
    assert graph is not None
    # The compiled graph should have a 'chatbot' node
    assert "chatbot" in graph.get_graph().nodes


@patch("src.langgraphagenticai.graph.graph_builder.get_tools")
def test_setup_graph_chatbot_with_tool(mock_get_tools):
    """setup_graph('Chatbot with Tool') must return a compiled graph with 'chatbot' and 'tools' nodes."""
    mock_get_tools.return_value = []
    mock_llm = MockLLM()
    builder = GraphBuilder(mock_llm)
    graph = builder.setup_graph("Chatbot with Tool")
    assert graph is not None
    nodes = graph.get_graph().nodes
    assert "chatbot" in nodes
    assert "tools" in nodes


def test_setup_graph_unknown_usecase_raises():
    """setup_graph with an unknown use case must raise ValueError (empty graph cannot compile)."""
    mock_llm = MockLLM()
    builder = GraphBuilder(mock_llm)
    try:
        builder.setup_graph("Unknown Usecase")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
