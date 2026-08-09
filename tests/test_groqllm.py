"""Tests for the GroqLLM class."""
from unittest.mock import patch, MagicMock

from src.langgraphagenticai.LLMS.groqllm import GroqLLM


def test_get_llm_model_returns_none_when_api_key_empty():
    """get_llm_model() must return None and show an error when the API key is empty."""
    with patch("streamlit.error") as mock_error:
        llm_config = GroqLLM(
            user_controls_input={
                "GROQ_API_KEY": "",
                "selected_groq_model": "llama3-8b-8192",
            }
        )
        result = llm_config.get_llm_model()
        assert result is None
        mock_error.assert_called_once()


@patch("src.langgraphagenticai.LLMS.groqllm.ChatGroq", side_effect=Exception("connection error"))
def test_get_llm_model_raises_on_exception(mock_chat_groq):
    """get_llm_model() must raise ValueError when ChatGroq initialization fails."""
    llm_config = GroqLLM(
        user_controls_input={
            "GROQ_API_KEY": "fake-key",
            "selected_groq_model": "llama3-8b-8192",
        }
    )
    try:
        llm_config.get_llm_model()
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


@patch("src.langgraphagenticai.LLMS.groqllm.ChatGroq")
def test_get_llm_model_returns_llm_when_api_key_provided(mock_chat_groq):
    """get_llm_model() must return a ChatGroq instance when a valid API key is provided."""
    mock_instance = MagicMock()
    mock_chat_groq.return_value = mock_instance
    llm_config = GroqLLM(
        user_controls_input={
            "GROQ_API_KEY": "fake-key",
            "selected_groq_model": "llama3-8b-8192",
        }
    )
    result = llm_config.get_llm_model()
    assert result is mock_instance
    mock_chat_groq.assert_called_once_with(
        api_key="fake-key", model="llama3-8b-8192"
    )
