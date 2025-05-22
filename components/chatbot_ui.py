import streamlit as st

def chat_input():
    return st.text_input("Ask a financial question:", key="chat_input")

def chat_display(history):
    for user, bot in history:
        st.markdown(f"**You:** {user}")
        st.markdown(f"**Aureus:** {bot}")
