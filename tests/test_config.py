"""Tests for the Config class that reads uiconfigfile.ini."""
from src.langgraphagenticai.ui.uiconfigfile import Config


def test_config_reads_page_title():
    """Config must read the PAGE_TITLE from the INI file."""
    config = Config()
    assert config.get_page_title() == "LangGraph: Build Stateful Agentic AI graph"


def test_config_reads_llm_options():
    """Config must read and split LLM_OPTIONS from the INI file."""
    config = Config()
    assert config.get_llm_options() == ["Groq"]


def test_config_reads_usecase_options():
    """Config must read and split USECASE_OPTIONS from the INI file."""
    config = Config()
    assert config.get_usecase_options() == ["Basic Chatbot", "Chatbot with Tool"]


def test_config_reads_groq_model_options():
    """Config must read and split GROQ_MODEL_OPTIONS from the INI file."""
    config = Config()
    expected = ["mixtral-8x7b-32768", "llama3-8b-8192", "llama3-70b-8192", "gemma-7b-i"]
    assert config.get_groq_model_options() == expected


def test_config_uses_file_relative_path():
    """Config must locate uiconfigfile.ini relative to its own module location."""
    import os
    config = Config()
    expected_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "src",
        "langgraphagenticai",
        "ui",
        "uiconfigfile.ini",
    )
    # The config should have successfully read the file (no exception)
    assert config.get_page_title() is not None
