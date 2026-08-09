import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    @staticmethod
    def display_chat_history(messages):
        """
        Displays pre-existing chat history stored in session_state.messages.
        """
        for message in messages:
            if isinstance(message, HumanMessage) or type(message) == HumanMessage:
                with st.chat_message("user"):
                    st.write(message.content)
            elif isinstance(message, ToolMessage) or type(message) == ToolMessage:
                with st.chat_message("assistant", avatar="🛠️"):
                    st.markdown("""
                    <div style="background-color: #161b22; border: 1px solid #30363d; border-left: 4px solid #d29922; border-radius: 6px; padding: 8px 12px; margin-bottom: 8px;">
                        <span style="color: #e3b341; font-weight: 700; font-size: 0.8rem; letter-spacing: 0.05em;">🛠️ TAVILY SEARCH TOOL EXECUTED</span>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("📄 View Tavily Search Tool Output", expanded=False):
                        try:
                            parsed = json.loads(message.content)
                            st.json(parsed)
                        except Exception:
                            st.code(message.content, language="json")
            elif isinstance(message, AIMessage) or type(message) == AIMessage:
                if message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)

    def display_result_on_ui(self):
        """
        Invokes the LangGraph StateGraph, updates session_state messages,
        and renders new messages including real Tavily tool execution output.
        """
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # Add human message object to session state
        human_msg = HumanMessage(content=user_message)
        st.session_state.messages.append(human_msg)

        # Display newly entered user message
        with st.chat_message("user"):
            st.write(user_message)

        # Execute LangGraph state graph
        with st.spinner("⚡ Executing LangGraph state graph flow..."):
            initial_state = {"messages": st.session_state.messages}
            res = graph.invoke(initial_state)

        # Update session state with graph state result
        updated_messages = res.get("messages", [])
        st.session_state.messages = updated_messages

        # Render newly generated messages (all messages after current human_msg)
        new_messages = []
        found_human = False
        for msg in updated_messages:
            if found_human:
                new_messages.append(msg)
            elif msg is human_msg or (isinstance(msg, HumanMessage) and msg.content == user_message):
                found_human = True

        # Fallback if matching object reference wasn't found
        if not new_messages and len(updated_messages) > 1:
            new_messages = [updated_messages[-1]]

        for message in new_messages:
            if isinstance(message, ToolMessage) or type(message) == ToolMessage:
                with st.chat_message("assistant", avatar="🛠️"):
                    st.markdown("""
                    <div style="background-color: #161b22; border: 1px solid #30363d; border-left: 4px solid #d29922; border-radius: 6px; padding: 8px 12px; margin-bottom: 8px;">
                        <span style="color: #e3b341; font-weight: 700; font-size: 0.8rem; letter-spacing: 0.05em;">🛠️ TAVILY SEARCH TOOL EXECUTED</span>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("📄 View Tavily Search Tool Output", expanded=True):
                        try:
                            parsed = json.loads(message.content)
                            st.json(parsed)
                        except Exception:
                            st.code(message.content, language="json")
            elif isinstance(message, AIMessage) or type(message) == AIMessage:
                if message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)

             
