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
from components.definitions import FinancialDefinitions

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
        self.definitions = FinancialDefinitions()
        
        # Initialize session state
        if 'current_data' not in st.session_state:
            st.session_state.current_data = None
        if 'user_id' not in st.session_state:
            st.session_state.user_id = "default_user"
    
    def run(self):
        """Main application runner"""
        st.title("Aureus - Application for Startups")
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio(
            "Go to",
            ["Dashboard", "Data Upload", "Forecasting", "Anomaly Detection", "AI Advisor", "Reports", "Understanding"]
        )
        
        # User ID input in sidebar
        st.sidebar.text_input("User ID", key="user_id", value=st.session_state.user_id)
        
        # Load data if available
        if st.session_state.current_data is not None:
            self.dashboard.load_data(st.session_state.current_data)
        
        # Page routing
        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Data Upload":
            self.show_data_upload()
        elif page == "Forecasting":
            self.show_forecasting()
        elif page == "Anomaly Detection":
            self.show_anomaly_detection()
        elif page == "AI Advisor":
            self.show_ai_advisor()
        elif page == "Reports":
            self.show_reports()
        elif page == "Understanding":
            self.show_understanding()
    
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
                # First, check for obvious anomalies
                obvious_anomalies = self.data_preprocessor.detect_anomalies(st.session_state.current_data)
                if not obvious_anomalies.empty:
                    st.warning("Found obvious anomalies in the data:")
                    st.dataframe(obvious_anomalies)
                
                # Then run the ML-based anomaly detection
                anomalies = self.anomaly_detector.detect(st.session_state.current_data)
                if not anomalies.empty:
                    st.warning(f"Found {len(anomalies)} ML-detected anomalies!")
                    st.dataframe(anomalies)
                    
                    # Option to send email alert
                    if st.button("Send Alert Email"):
                        email_sent = self.email_handler.send_alert(
                            recipient=os.getenv("ALERT_RECIPIENT"),
                            alert_type="Financial Anomaly",
                            alert_message=f"Found {len(anomalies)} anomalous transactions"
                        )
                        if email_sent:
                            st.success("Alert email sent!")
                else:
                    st.success("No ML-detected anomalies found")
    
    def show_ai_advisor(self):
        """Show AI advisor page"""
        st.header("AI Financial Advisor")
        self.advisor.render()
    
    def show_reports(self):
        """Show reporting page"""
        st.header("Financial Reports")
        
        if st.session_state.current_data is None:
            st.warning("Please upload data first from the Data Upload page")
            return
        
        report_type = st.selectbox("Report Type", ["Weekly", "Monthly", "Quarterly"])
        
        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                # Generate report content
                df = st.session_state.current_data
                total_expenses = df['amount'].sum()
                
                # Group by category
                category_totals = df.groupby('category')['amount'].sum().sort_values(ascending=False)
                
                # Group by department
                department_totals = df.groupby('department')['amount'].sum().sort_values(ascending=False)
                
                # Group by payment method
                payment_totals = df.groupby('payment_method')['amount'].sum().sort_values(ascending=False)
                
                report = f"""
                # {report_type} Financial Report
                
                ## Summary
                - Total Expenses: ${total_expenses:,.2f}
                
                ## Top Expense Categories
                {category_totals.head(5).to_markdown()}
                
                ## Department-wise Expenses
                {department_totals.to_markdown()}
                
                ## Payment Method Distribution
                {payment_totals.to_markdown()}
                
                ## Status Distribution
                {df['status'].value_counts().to_markdown()}
                """
                
                st.markdown(report)
                
                # Option to email report
                if st.button("Email This Report"):
                    email_sent = self.email_handler.send_report(
                        recipient=os.getenv("REPORT_RECIPIENT"),
                        report_type=report_type,
                        report_data=report
                    )
                    if email_sent:
                        st.success("Report emailed successfully!")

    def show_understanding(self):
        """Show the Understanding page with financial terms and definitions"""
        self.definitions.render()

if __name__ == "__main__":
    app = FinanceApp()
    app.run()