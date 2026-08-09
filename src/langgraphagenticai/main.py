import streamlit as st
import os
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit

# MAIN Function START
def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI.
    Initializes AI Studio UI, sidebar controls, visual workflow diagram,
    handles chat input, and executes graph workflow state flow.
    """

    # Load UI & Sidebar controls
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return

    # Render main header & visual workflow architecture diagram
    usecase = user_input.get("selected_usecase", "Basic Chatbot")
    ui.render_main_header(usecase)

    # Initialize messages list in session state if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display pre-existing chat history
    DisplayResultStreamlit.display_chat_history(st.session_state.messages)

    # Chat input field
    user_message = st.chat_input("Ask ⚡ LangGraph State Flow...")

    if user_message:
        # Validate API keys before execution
        groq_api_key = user_input.get("GROQ_API_KEY")
        if not groq_api_key:
            st.error("⚠️ GROQ_API_KEY is missing from Streamlit secrets / environment variables.")
            return

        if usecase == "Chatbot with Tool" and not user_input.get("TAVILY_API_KEY"):
            st.error("⚠️ TAVILY_API_KEY is missing from Streamlit secrets / environment variables.")
            return

        # Ensure environment variables are active
        if groq_api_key:
            os.environ["GROQ_API_KEY"] = groq_api_key
        if user_input.get("TAVILY_API_KEY"):
            os.environ["TAVILY_API_KEY"] = user_input["TAVILY_API_KEY"]

        try:
            # Configure LLM
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized.")
                return

            # Initialize and set up graph based on use case
            graph_builder = GraphBuilder(model)
            try:
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            except Exception as e:
                st.error(f"Error: Graph setup failed - {e}")
                return

        except Exception as e:
            st.error(f"Error Occurred with Exception : {e}")

