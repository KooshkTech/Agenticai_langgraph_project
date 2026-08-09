import streamlit as st
import os
from src.langgraphagenticai.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def inject_custom_css(self):
        """
        Injects professional dark AI Studio design styling into Streamlit.
        Palette:
        - background: #0d1117
        - sidebar: #161b22
        - borders: #30363d
        - text: #c9d1d9
        """
        st.markdown("""
        <style>
        /* Base page background & typography */
        .stApp {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 1px solid #30363d !important;
        }

        [data-testid="stSidebar"] * {
            color: #c9d1d9 !important;
        }

        /* Input fields, selectboxes, text inputs */
        div[data-baseweb="select"] > div,
        input[type="text"],
        input[type="password"],
        textarea {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
        }

        div[data-baseweb="select"] span {
            color: #c9d1d9 !important;
        }

        /* Header background */
        header[data-testid="stHeader"] {
            background-color: #0d1117 !important;
        }

        /* Studio card styling */
        .studio-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 12px 14px;
            margin-bottom: 12px;
        }

        .studio-card-title {
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #8b949e;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .studio-card-value {
            font-size: 0.9rem;
            font-weight: 600;
            color: #58a6ff;
            word-break: break-word;
        }

        .studio-card-desc {
            font-size: 0.78rem;
            color: #8b949e;
            margin-top: 4px;
        }

        /* Badges */
        .badge-ready {
            background-color: rgba(35, 134, 54, 0.2);
            color: #3fb950;
            border: 1px solid rgba(46, 160, 67, 0.4);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.72rem;
            font-weight: 600;
        }

        .badge-warning {
            background-color: rgba(210, 153, 34, 0.2);
            color: #d29922;
            border: 1px solid rgba(210, 153, 34, 0.4);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.72rem;
            font-weight: 600;
        }

        .badge-info {
            background-color: rgba(56, 139, 253, 0.15);
            color: #58a6ff;
            border: 1px solid rgba(56, 139, 253, 0.4);
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.72rem;
            font-weight: 600;
        }

        /* Workflow diagram container */
        .workflow-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 20px;
        }

        .workflow-title {
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #8b949e;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .diagram-flow {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .node-box {
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 6px 12px;
            font-size: 0.78rem;
            font-weight: 600;
            color: #c9d1d9;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .node-start {
            border-color: #238636;
            color: #3fb950;
            background-color: rgba(35, 134, 54, 0.1);
        }

        .node-chatbot {
            border-color: #388bfd;
            color: #58a6ff;
            background-color: rgba(56, 139, 253, 0.1);
        }

        .node-condition {
            border-color: #8957e5;
            color: #bc8cff;
            background-color: rgba(137, 87, 229, 0.1);
        }

        .node-tool {
            border-color: #d29922;
            color: #e3b341;
            background-color: rgba(210, 153, 34, 0.1);
        }

        .node-end {
            border-color: #f85149;
            color: #ff7b72;
            background-color: rgba(248, 81, 73, 0.1);
        }

        .arrow-connector {
            color: #8b949e;
            font-weight: bold;
            font-size: 0.9rem;
        }

        /* Buttons */
        .stButton > button {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
            width: 100%;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            background-color: #30363d !important;
            border-color: #8b949e !important;
            color: #ffffff !important;
        }

        /* Chat input styling */
        [data-testid="stChatInput"] {
            border-color: #30363d !important;
            background-color: #161b22 !important;
        }
        </style>
        """, unsafe_allow_html=True)

    def load_streamlit_ui(self):
        """
        Loads the Streamlit UI with sidebar settings, cards, and state tracking.
        """
        st.set_page_config(
            page_title="⚡ LangGraph State Flow",
            page_icon="⚡",
            layout="wide"
        )
        self.inject_custom_css()

        # Initialize session state keys if missing
        if "GROQ_API_KEY" not in st.session_state:
            st.session_state["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "")
        if "TAVILY_API_KEY" not in st.session_state:
            st.session_state["TAVILY_API_KEY"] = os.environ.get("TAVILY_API_KEY", "")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        with st.sidebar:
            st.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <span style="font-size: 1.5rem;">⚡</span>
                <span style="font-size: 1.2rem; font-weight: 700; color: #f0f6fc; letter-spacing: -0.02em;">LangGraph State Flow</span>
            </div>
            <div style="font-size: 0.78rem; color: #8b949e; margin-bottom: 16px;">
                Professional AI Studio Architecture
            </div>
            """, unsafe_allow_html=True)

            # LLM selection
            llm_options = self.config.get_llm_options()
            self.user_controls["selected_llm"] = st.selectbox("LLM Provider", llm_options)

            # Groq model settings
            model_options = self.config.get_groq_model_options()
            self.user_controls["selected_groq_model"] = st.selectbox(
                "Groq Model Settings",
                model_options,
                help="Supported active Groq production models"
            )

            # API Key Configuration
            st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#8b949e; text-transform:uppercase; margin-top:12px; margin-bottom:6px;'>API Configuration</div>", unsafe_allow_html=True)

            groq_key_input = st.text_input(
                "Groq API Key",
                value=st.session_state["GROQ_API_KEY"],
                type="password",
                placeholder="gsk_..."
            )
            self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = groq_key_input
            if groq_key_input:
                os.environ["GROQ_API_KEY"] = groq_key_input

            tavily_key_input = st.text_input(
                "Tavily API Key",
                value=st.session_state["TAVILY_API_KEY"],
                type="password",
                placeholder="tvly-..."
            )
            self.user_controls["TAVILY_API_KEY"] = st.session_state["TAVILY_API_KEY"] = tavily_key_input
            if tavily_key_input:
                os.environ["TAVILY_API_KEY"] = tavily_key_input

            # Workflow selector
            st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#8b949e; text-transform:uppercase; margin-top:12px; margin-bottom:6px;'>Workflow Selection</div>", unsafe_allow_html=True)
            usecase_options = self.config.get_usecase_options()
            self.user_controls["selected_usecase"] = st.selectbox("Workflow Selector", usecase_options)

            selected_usecase = self.user_controls["selected_usecase"]
            groq_ready = bool(self.user_controls["GROQ_API_KEY"])
            tavily_ready = bool(self.user_controls["TAVILY_API_KEY"])

            # System Status Card
            groq_badge = '<span class="badge-ready">READY</span>' if groq_ready else '<span class="badge-warning">KEY REQUIRED</span>'
            if selected_usecase == "Chatbot with Tool":
                tavily_badge = '<span class="badge-ready">READY</span>' if tavily_ready else '<span class="badge-warning">KEY REQUIRED</span>'
            else:
                tavily_badge = '<span class="badge-info">OPTIONAL</span>'

            st.markdown(f"""
            <div class="studio-card">
                <div class="studio-card-title">⚙️ System Status</div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; font-size:0.8rem;">
                    <span>Groq LLM Engine:</span>
                    {groq_badge}
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.8rem;">
                    <span>Tavily Search API:</span>
                    {tavily_badge}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Active Workflow Card
            nodes_desc = "START ➔ CHATBOT ➔ END" if selected_usecase == "Basic Chatbot" else "START ➔ CHATBOT ➔ TOOLS CONDITION ➔ TAVILY SEARCH ➔ CHATBOT ➔ END"
            st.markdown(f"""
            <div class="studio-card">
                <div class="studio-card-title">🔀 Active Workflow</div>
                <div class="studio-card-value">{selected_usecase}</div>
                <div class="studio-card-desc">{nodes_desc}</div>
            </div>
            """, unsafe_allow_html=True)

            # Selected Model Card
            selected_model = self.user_controls["selected_groq_model"]
            st.markdown(f"""
            <div class="studio-card">
                <div class="studio-card-title">🤖 Selected Model</div>
                <div class="studio-card-value">Groq / {selected_model}</div>
                <div class="studio-card-desc">Provider: ChatGroq • Status: Active</div>
            </div>
            """, unsafe_allow_html=True)

            # Graph State Card
            msg_count = len(st.session_state.get("messages", []))
            st.markdown(f"""
            <div class="studio-card">
                <div class="studio-card-title">📊 Graph State</div>
                <div class="studio-card-value">{msg_count} Message(s)</div>
                <div class="studio-card-desc">Reducer: <code>add_messages</code> • State: <code>StateGraph</code></div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🗑️ Clear Conversation"):
                st.session_state.messages = []
                st.rerun()

        return self.user_controls

    def render_main_header(self, usecase):
        """
        Renders application branding header and live visual workflow diagram.
        """
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #30363d; padding-bottom: 12px; margin-bottom: 16px;">
            <div>
                <h1 style="font-size: 1.6rem; font-weight: 800; color: #f0f6fc; margin: 0; display: flex; align-items: center; gap: 8px;">
                    ⚡ LangGraph State Flow
                </h1>
                <p style="font-size: 0.85rem; color: #8b949e; margin: 4px 0 0 0;">
                    Enterprise State Machine Architecture powered by LangGraph & Groq
                </p>
            </div>
            <div>
                <span class="badge-info" style="font-size:0.8rem; padding: 4px 10px;">AI STUDIO ACTIVE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Visual Workflow Diagram
        if usecase == "Basic Chatbot":
            st.markdown("""
            <div class="workflow-card">
                <div class="workflow-title">
                    <span>🌐 Visual Workflow Diagram: Basic Chatbot</span>
                </div>
                <div class="diagram-flow">
                    <div class="node-box node-start">▶ START</div>
                    <span class="arrow-connector">➔</span>
                    <div class="node-box node-chatbot">🤖 CHATBOT NODE</div>
                    <span class="arrow-connector">➔</span>
                    <div class="node-box node-end">⏹ END</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="workflow-card">
                <div class="workflow-title">
                    <span>🌐 Visual Workflow Diagram: Tavily Search Workflow</span>
                </div>
                <div class="diagram-flow">
                    <div class="node-box node-start">▶ START</div>
                    <span class="arrow-connector">➔</span>
                    <div class="node-box node-chatbot">🤖 CHATBOT NODE</div>
                    <span class="arrow-connector">➔</span>
                    <div class="node-box node-condition">🔀 TOOLS CONDITION</div>
                    <span class="arrow-connector">➔</span>
                    <div class="node-box node-tool">🔍 TAVILY SEARCH (ToolNode)</div>
                    <span class="arrow-connector">➔</span>
                    <div class="node-box node-chatbot">🤖 CHATBOT NODE</div>
                    <span class="arrow-connector">➔</span>
                    <div class="node-box node-end">⏹ END</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

