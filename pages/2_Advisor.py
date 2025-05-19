import streamlit as st
from models import llm_agent
from components import chatbot_ui

# Minimal advisor page

def show():
    st.header("💬 AI Financial Advisor")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_input = chatbot_ui.chat_input()
    if user_input:
        response = llm_agent.ask(user_input, st.session_state['chat_history'])
        st.session_state['chat_history'].append((user_input, response))

    chatbot_ui.chat_display(st.session_state['chat_history'])
