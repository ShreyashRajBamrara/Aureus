import streamlit as st
import pandas as pd
from utils.email_handler import EmailHandler

class EmailCenter:
    def __init__(self):
        self.email_handler = EmailHandler()
        if 'anomalies' not in st.session_state:
            st.session_state.anomalies = pd.DataFrame()

    def render(self):
        st.header("Email Notification Center")

        anomalies = st.session_state.anomalies

        if anomalies.empty:
            st.warning("No anomalies have been detected yet. Please run anomaly detection first.")
            return

        st.subheader("Detected Anomalies Requiring Attention")
        st.dataframe(anomalies)

        st.subheader("Send Anomaly Alert")
        
        employee_list = anomalies['Employee Name'].unique().tolist()
        
        if not employee_list:
            st.info("No employees associated with the current anomalies.")
            return

        selected_employee = st.selectbox("Select Employee to Notify", options=employee_list)
        
        anomaly_to_report = anomalies[anomalies['Employee Name'] == selected_employee]

        if not anomaly_to_report.empty:
            st.write(f"Anomalies for {selected_employee}:")
            selected_anomaly_index = st.radio(
                "Select an anomaly to report:",
                anomaly_to_report.index,
                format_func=lambda x: f"Anomaly on {anomaly_to_report.loc[x]['Date']} for ${anomaly_to_report.loc[x]['Amount']}"
            )
            
            selected_anomaly_details = anomaly_to_report.loc[selected_anomaly_index]
            st.write("Details:")
            st.write(selected_anomaly_details)

            default_message = "Please review this transaction and provide an explanation. This transaction was flagged as a potential anomaly."
            custom_message = st.text_area("Add a custom message (optional):", value=default_message, key=f"custom_message_{selected_employee}")

            if st.button(f"Send Alert to {selected_employee}"):
                success = self.email_handler.send_anomaly_alert(
                    recipient_email=selected_anomaly_details['Email'],
                    employee_name=selected_employee,
                    anomaly_details=selected_anomaly_details.to_dict(),
                    custom_message=custom_message
                )
                if success:
                    st.success(f"Alert sent to {selected_employee}!")
                else:
                    st.error("Failed to send alert. Please check email credentials in your .env file.")
        else:
            st.warning(f"No anomalies detected for {selected_employee}.") 