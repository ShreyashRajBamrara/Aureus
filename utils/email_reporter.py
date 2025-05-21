import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import streamlit as st # Keep st import for error messages in this case

def send_anomaly_email(recipient_email, anomaly_data):
    try:
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASSWORD')
        
        if not all([sender_email, sender_password]):
            st.error("Email credentials not configured. Please set EMAIL_USER and EMAIL_PASSWORD in .env file.")
            return False
            
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Expense Anomaly Alert"
        
        # Create email body
        body = f"""
Dear {anomaly_data.get('Employee Name', 'recipient')},

We have detected the following anomaly in your expense submission:

Date: {anomaly_data.get('Date', 'N/A')}
Amount: ₹{anomaly_data.get('Amount', 0.0):,.2f}
Vendor: {anomaly_data.get('Vendor', 'N/A')}
Category: {anomaly_data.get('Category', 'N/A')}
Anomaly Type: {anomaly_data.get('Anomaly_Type', 'N/A')}
Notes: {anomaly_data.get('Notes', 'N/A')}

Please review this expense and provide additional information if needed.

Best regards,
Aureus Finance Team
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False 