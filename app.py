import streamlit as st
from components.sidebar import show_sidebar
import importlib

# Set Streamlit page config
st.set_page_config(page_title="Aureus for Startups", layout="wide")

# Show sidebar navigation
page = show_sidebar()

# Page routing
if page == "Dashboard":
    dashboard = importlib.import_module("pages.1_Dashboard")
    dashboard.show()
elif page == "Advisor":
    advisor = importlib.import_module("pages.2_Advisor")
    advisor.show()
elif page == "FraudWatch":
    fraudwatch = importlib.import_module("pages.3_FraudWatch")
    fraudwatch.show()
else:
    st.write("Select a page from the sidebar.")
