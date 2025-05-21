import streamlit as st
import os
from dotenv import load_dotenv

# Import page functions
from pages.dashboard_page import dashboard_page
from pages.advisor_page import advisor_page
from pages.analysis_report_page import analysis_report_page

# Load environment variables
load_dotenv()

# Set Streamlit page config
st.set_page_config(
    page_title="Aureus for Startups",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
CURRENT_CASH = float(os.getenv('CURRENT_CASH', 10000000))  # Default 10M if not set

# Sidebar for navigation
st.sidebar.title("Aureus for Startups")
page = st.sidebar.radio(
    "Navigation",
    ("Dashboard", "Advisor", "Analysis and Report"),
    index=0
)
st.sidebar.markdown("---")
st.sidebar.info("AI Finance Assistant for Startups")

# Main content based on selected page
if page == "Dashboard":
    dashboard_page()

elif page == "Advisor":
    advisor_page()

elif page == "Analysis and Report":
    analysis_report_page()

# Run the app
if __name__ == "__main__":
    pass
