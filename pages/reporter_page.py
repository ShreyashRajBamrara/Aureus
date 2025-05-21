import streamlit as st
from utils.data_processing import load_and_process_data
from utils.anomaly_detection import detect_anomalies
from utils.email_reporter import send_anomaly_email

def reporter_page():
    st.title("Anomaly Reporter")
    
    df = load_and_process_data()
    if df is not None:
        # Get anomalies
        anomalies = detect_anomalies(df)
        
        if not anomalies.empty:
            st.subheader("Detected Anomalies")
            
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
                recipient_email = st.text_input("Recipient Email", value=anomaly_data['Employee Name'])
                message = st.text_area("Additional Message", 
                                     "Please review this expense and provide additional information if needed.")
                
                if st.button("Send Report"):
                    if send_anomaly_email(recipient_email, anomaly_data):
                        st.success("Report sent successfully!")
                    else:
                        st.error("Failed to send report. Please check email configuration.")
        else:
            st.info("No anomalies detected in the current dataset.") 