import streamlit as st
import pandas as pd
from utils.data_processing import load_and_process_data
from utils.anomaly_detection import detect_anomalies
from utils.email_reporter import send_anomaly_email

def analysis_report_page():
    st.title("Anomaly Analysis and Reporting")
    
    df = load_and_process_data()
    
    if df is not None:
        st.subheader("Detected Anomalies")
        anomalies = detect_anomalies(df)
        
        if not anomalies.empty:
            st.warning(f"Found {len(anomalies)} potential anomalies in your financial data.")
            
            # Group anomalies by Department and Employee
            st.subheader("Anomalies by Department")
            dept_anomalies = anomalies.groupby('Department').agg(list).reset_index()
            for index, row in dept_anomalies.iterrows():
                department = row['Department']
                st.write(f"#### {department}")
                dept_anomaly_data = pd.DataFrame(row['Amount'])
                # Reconstruct DataFrame for display
                dept_anomaly_df = anomalies[anomalies['Department'] == department].copy()
                st.dataframe(dept_anomaly_df[["Date", "Expense ID", "Amount", "Category", "Vendor", "Employee Name", "Anomaly_Type", "Notes"]])
                
            st.subheader("Anomalies by Employee")
            emp_anomalies = anomalies.groupby('Employee Name').agg(list).reset_index()
            for index, row in emp_anomalies.iterrows():
                employee = row['Employee Name']
                st.write(f"#### {employee}")
                 # Reconstruct DataFrame for display
                emp_anomaly_df = anomalies[anomalies['Employee Name'] == employee].copy()
                st.dataframe(emp_anomaly_df[["Date", "Expense ID", "Amount", "Category", "Vendor", "Department", "Anomaly_Type", "Notes"]])
            
            st.subheader("Report Anomalies via Email")
            
            # Select anomaly to report
            anomaly_options = [f"{row['Date']} - ₹{row['Amount']:,.2f} - {row['Vendor']} - {row['Anomaly_Type']}" 
                             for _, row in anomalies.iterrows()]
            selected_anomaly = st.selectbox("Select Anomaly to Report", anomaly_options)
            
            if selected_anomaly:
                # Get the corresponding anomaly data
                selected_idx = anomaly_options.index(selected_anomaly)
                anomaly_data = anomalies.iloc[selected_idx]
                
                # Display anomaly details
                st.write("### Anomaly Details")
                st.write(f"Date: {anomaly_data['Date']}")
                st.write(f"Amount: ₹{anomaly_data['Amount']:,.2f}")
                st.write(f"Vendor: {anomaly_data['Vendor']}")
                st.write(f"Category: {anomaly_data['Category']}")
                st.write(f"Employee: {anomaly_data['Employee Name']}")
                st.write(f"Anomaly Type: {anomaly_data['Anomaly_Type']}")
                
                # Email form
                st.write("### Send Report")
                # Pre-fill recipient email if Employee Name looks like an email address, otherwise leave blank
                initial_email = anomaly_data['Employee Name'] if '@' in str(anomaly_data['Employee Name']) else ''
                recipient_email = st.text_input("Recipient Email", value=initial_email)
                message = st.text_area("Additional Message", 
                                     "Please review this expense and provide additional information if needed.")
                
                if st.button("Send Report"):
                    if recipient_email:
                        if send_anomaly_email(recipient_email, anomaly_data):
                            st.success("Report sent successfully!")
                        else:
                            st.error("Failed to send report. Please check email configuration and recipient address.")
                    else:
                        st.warning("Please enter a recipient email address.")
        else:
            st.info("No anomalies detected in the current dataset.") 