import streamlit as st
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

# Import components
from components.dashboard import Dashboard
from utils.email_handler import EmailHandler
from utils.file_handling import FileHandler
from utils.data_preprocessor import DataPreprocessor
from components.advisor import AIAdvisor
from components.forecasting import FinancialForecaster
from components.anomaly import AnomalyDetector
from components.email_center import EmailCenter

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Aureus",
    
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create necessary directories
Path("data/processed").mkdir(parents=True, exist_ok=True)
Path("data/chat_history").mkdir(parents=True, exist_ok=True)

class FinanceApp:
    def __init__(self):
        self.file_handler = FileHandler()
        self.email_handler = EmailHandler()
        self.dashboard = Dashboard()
        self.advisor = AIAdvisor()
        self.forecaster = FinancialForecaster()
        self.anomaly_detector = AnomalyDetector()
        self.data_preprocessor = DataPreprocessor()
        self.email_center = EmailCenter()
        
        # Initialize session state
        if 'current_data' not in st.session_state:
            st.session_state.current_data = None
        if 'user_id' not in st.session_state:
            st.session_state.user_id = "default_user"
        if 'anomalies' not in st.session_state:
            st.session_state.anomalies = None
    
    def run(self):
        """Main application runner"""
        st.title("Aureus - Application for Startups")
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio(
            "Go to",
            ["Home", "Data Upload", "Dashboard", "Forecasting", "Anomaly Detection", "Email Center", "AI Advisor"]
        )
        
        # User ID input in sidebar
        if 'user_id' not in st.session_state:
            st.session_state.user_id = "default_user"
        st.sidebar.text_input("User ID", key="user_id")
        
        # Load data if available
        if st.session_state.current_data is not None:
            self.dashboard.load_data(st.session_state.current_data)
        
        # Page routing
        if page == "Home":
            self.show_home()
        elif page == "Data Upload":
            self.show_data_upload()
        elif page == "Dashboard":
            self.show_dashboard()
        elif page == "Forecasting":
            self.show_forecasting()
        elif page == "Anomaly Detection":
            self.show_anomaly_detection()
        elif page == "Email Center":
            self.show_email_center()
        elif page == "AI Advisor":
            self.show_ai_advisor()
    
    def show_home(self):
        st.header("Welcome to Aureus!")
        st.markdown("""
        **Aureus** is your all-in-one financial analysis and anomaly detection system for startups and businesses.
        
        ### Key Features
        - **Data Upload:** Easily upload your financial transaction data (CSV format).
        - **Dashboard:** Visualize your financial health with interactive charts and summaries.
        - **Forecasting:** Predict future trends using advanced forecasting models.
        - **Anomaly Detection:** Automatically flag unusual or suspicious transactions.
        - **Email Center:** Instantly notify team members about anomalies via email.
        - **AI Advisor:** Get AI-powered financial advice and insights.
        
        ### How It Works
        1. **Upload your data** on the Data Upload page.
        2. **Explore your finances** on the Dashboard.
        3. **Run forecasting** to see future trends.
        4. **Detect anomalies** and review flagged transactions.
        5. **Send alerts** to relevant people from the Email Center.
        6. **Ask questions** or get help from the AI Advisor.
        
        > **Tip:** Use the sidebar to navigate between features. Start with Data Upload!
        """)
    
    def show_dashboard(self):
        """Render the dashboard page"""
        st.header("Financial Dashboard")
        
        if st.session_state.current_data is not None:
            self.dashboard.render()
        else:
            st.warning("Please upload data first from the Data Upload page")
    
    def show_data_upload(self):
        """Handle data upload and processing"""
        st.header("Data Upload")
        
        # Add option to use sample data
        use_sample = st.checkbox("Use Sample Aureus Expenditure Data")
        
        if use_sample:
            try:
                # Load the sample data
                df = pd.read_csv("data/aureus_expenditure_with_anomalies.csv")
                
                # Store the raw data for anomaly detection
                st.session_state.raw_data = df.copy()
                
                # Preprocess the data
                processed_df = self.data_preprocessor.preprocess_aureus_data(df)
                
                # Validate the processed data
                is_valid, validation_message = self.data_preprocessor.validate_processed_data(processed_df)
                if not is_valid:
                    st.error(validation_message)
                    return
                
                # Store the data
                st.session_state.current_data = processed_df
                st.success("Sample data loaded and processed successfully!")
                
                # Show preview
                with st.expander("View Data Preview"):
                    st.dataframe(processed_df.head())
                
                # Save processed file
                success, save_error = self.file_handler.save_processed_data(processed_df, "aureus_processed.csv")
                if not success:
                    st.warning(f"Couldn't save processed data: {save_error}")
                
            except Exception as e:
                st.error(f"Error processing sample data: {str(e)}")
        else:
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            if uploaded_file is not None:
                try:
                    # Read and validate the file
                    df = pd.read_csv(uploaded_file)
                    
                    # Preprocess the data
                    processed_df = self.data_preprocessor.preprocess_aureus_data(df)
                    
                    # Validate the processed data
                    is_valid, validation_message = self.data_preprocessor.validate_processed_data(processed_df)
                    if not is_valid:
                        st.error(validation_message)
                        return
                    
                    # Store the data
                    st.session_state.current_data = processed_df
                    st.success("Data loaded and processed successfully!")
                    
                    # Show preview
                    with st.expander("View Data Preview"):
                        st.dataframe(processed_df.head())
                    
                    # Save processed file
                    success, save_error = self.file_handler.save_processed_data(processed_df, "processed_data.csv")
                    if not success:
                        st.warning(f"Couldn't save processed data: {save_error}")
                    
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
    
    def show_forecasting(self):
        """Show forecasting page"""
        st.header("Financial Forecasting")
        
        if st.session_state.current_data is None:
            st.warning("Please upload data first from the Data Upload page")
            return
        
        # Add forecast period selection
        periods = st.slider("Forecast Period (days)", 7, 90, 30)
        
        if st.button("Generate Forecast"):
            with st.spinner("Generating forecasts..."):
                self.forecaster.render_forecast(st.session_state.current_data, periods)
    
    def show_anomaly_detection(self):
        """Show anomaly detection page"""
        st.header("Anomaly Detection")
        
        if st.session_state.current_data is None:
            st.warning("Please upload data first from the Data Upload page")
            return
        
        # Add contamination slider
        contamination = st.slider("Anomaly Detection Sensitivity", 0.01, 0.2, 0.1, 0.01)
        self.anomaly_detector = AnomalyDetector(contamination=contamination)
        
        if st.button("Run Anomaly Detection"):
            with st.spinner("Detecting anomalies..."):
                if 'raw_data' in st.session_state:
                    raw_df = st.session_state.raw_data
                    anomalies = self.anomaly_detector.detect(raw_df)
                    st.session_state.anomalies = anomalies
                    self.anomaly_detector.display_anomalies(anomalies)
                else:
                    st.warning("Please upload or select sample data first.")
    
    def show_email_center(self):
        """Show email center page"""
        st.header("Email Center")
        self.email_center.render()
    
    def show_ai_advisor(self):
        """Show AI advisor page"""
        st.header("AI Financial Advisor")
        self.advisor.render()

if __name__ == "__main__":
    app = FinanceApp()
    app.run()