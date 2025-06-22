import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailHandler:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        if not self.sender_email or not self.sender_password:
            logger.warning("Email credentials not found in environment variables")

    def send_anomaly_alert(self, recipient_email, employee_name, anomaly_details, custom_message=None):
        subject = f"Anomaly Alert for {employee_name}"
        body = f"""
        Dear {employee_name},

        An anomaly was detected in your recent transaction:
        {anomaly_details}

        {custom_message or 'Please review this transaction.'}

        Regards,
        Aureus Finance Team
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            logger.info(f"Email sent to {recipient_email}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False 