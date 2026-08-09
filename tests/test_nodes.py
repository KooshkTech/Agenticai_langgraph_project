"""Tests for the chatbot node classes."""
from unittest.mock import MagicMock

from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.nodes.chatbot_with_Tool_node import ChatbotWithToolNode


class MockLLM:
    """Minimal mock LLM that satisfies the interface used by the nodes."""

    def __init__(self, response="mock response"):
        self.response = response
        self.bound_tools = None

    def invoke(self, messages):
        return self.response

    def bind_tools(self, tools):
        self.bound_tools = tools
        return self


def test_basic_chatbot_node_process_returns_messages():
    """BasicChatbotNode.process() must return a dict with a 'messages' key."""
    mock_llm = MockLLM(response="hello from mock")
    node = BasicChatbotNode(mock_llm)
    result = node.process({"messages": []})
    assert "messages" in result
    assert result["messages"] == "hello from mock"


def test_basic_chatbot_node_uses_llm_invoke():
    """BasicChatbotNode.process() must call llm.invoke with the state messages."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "response"
    node = BasicChatbotNode(mock_llm)
    node.process({"messages": ["msg1", "msg2"]})
    mock_llm.invoke.assert_called_once_with(["msg1", "msg2"])


def test_chatbot_with_tool_node_create_chatbot_returns_callable():
    """ChatbotWithToolNode.create_chatbot() must return a callable node function."""
    mock_llm = MockLLM()
    node = ChatbotWithToolNode(mock_llm)
    chatbot = node.create_chatbot(tools=[])
    assert callable(chatbot)


def test_chatbot_with_tool_node_binds_tools():
    """create_chatbot() must call llm.bind_tools with the provided tools."""
    mock_llm = MagicMock()
    mock_llm.bind_tools.return_value = mock_llm
    mock_llm.invoke.return_value = "tool response"
    node = ChatbotWithToolNode(mock_llm)
    tools = ["tool1", "tool2"]
    chatbot = node.create_chatbot(tools)
    mock_llm.bind_tools.assert_called_once_with(tools)


def test_chatbot_with_tool_node_invoke_returns_messages():
    """The chatbot node function must return a dict with a 'messages' key."""
    mock_llm = MockLLM(response="tool-aware response")
    node = ChatbotWithToolNode(mock_llm)
    chatbot = node.create_chatbot(tools=[])
    result = chatbot({"messages": []})
    assert "messages" in result
    assert result["messages"] == ["tool-aware response"]
