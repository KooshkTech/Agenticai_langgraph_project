import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input['GROQ_API_KEY']
            selected_groq_model = self.user_controls_input['selected_groq_model']

            if not groq_api_key:
                st.error("Please enter your Groq API key to proceed.")
                return None

            llm = ChatGroq(api_key=groq_api_key, model=selected_groq_model)
            return llm

        except Exception as e:
            raise ValueError(f"Error occurred while initializing the Groq LLM: {e}")
