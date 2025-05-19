import streamlit as st

def show_sidebar():
    st.sidebar.title("Aureus for Startups")
    page = st.sidebar.radio(
        "Go to",
        ("Dashboard", "Advisor", "FraudWatch"),
        format_func=lambda x: x
    )
    st.sidebar.markdown("---")
    st.sidebar.info("AI Finance Assistant for Startups")
    return page
