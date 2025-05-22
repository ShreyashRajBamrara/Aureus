import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from typing import List, Optional
import logging
from dotenv import load_dotenv
from datetime import datetime

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
    
    def _create_message(self, recipient, subject, body, attachments=None):
        """Create email message with optional attachments"""
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachments if any
        if attachments:
            for attachment in attachments:
                with open(attachment, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                    msg.attach(part)
        
        return msg
    
    def _send_email(self, msg):
        """Send email using SMTP"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            return True
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_alert(self, recipient, alert_type, alert_message):
        """Send alert email"""
        if not all([self.sender_email, self.sender_password]):
            logger.warning("Email credentials not configured")
            return False
        
        subject = f"Financial Alert: {alert_type}"
        body = f"""
        Financial Alert
        
        Type: {alert_type}
        Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Message:
        {alert_message}
        
        This is an automated message from your Finance Application.
        """
        
        msg = self._create_message(recipient, subject, body)
        return self._send_email(msg)
    
    def send_report(self, recipient, report_type, report_data, attachments=None):
        """Send financial report email"""
        if not all([self.sender_email, self.sender_password]):
            logger.warning("Email credentials not configured")
            return False
        
        subject = f"Financial Report: {report_type}"
        body = f"""
        Financial Report
        
        Type: {report_type}
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Report Content:
        {report_data}
        
        This is an automated report from your Finance Application.
        """
        
        msg = self._create_message(recipient, subject, body, attachments)
        return self._send_email(msg)
    
    def send_weekly_summary(self, recipient, summary_data):
        """Send weekly financial summary"""
        if not all([self.sender_email, self.sender_password]):
            logger.warning("Email credentials not configured")
            return False
        
        subject = "Weekly Financial Summary"
        body = f"""
        Weekly Financial Summary
        
        Period: {datetime.now().strftime('%Y-%m-%d')}
        
        Summary:
        {summary_data}
        
        This is your weekly automated summary from the Finance Application.
        """
        
        msg = self._create_message(recipient, subject, body)
        return self._send_email(msg)
    
    def send_monthly_report(self, recipient, report_data, attachments=None):
        """Send monthly financial report"""
        if not all([self.sender_email, self.sender_password]):
            logger.warning("Email credentials not configured")
            return False
        
        subject = "Monthly Financial Report"
        body = f"""
        Monthly Financial Report
        
        Month: {datetime.now().strftime('%B %Y')}
        
        Report Content:
        {report_data}
        
        This is your monthly automated report from the Finance Application.
        """
        
        msg = self._create_message(recipient, subject, body, attachments)
        return self._send_email(msg)
    
    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """
        Send an email with optional attachments.
        
        Args:
            recipient: Email address of the recipient
            subject: Email subject
            body: Email body text
            attachments: List of file paths to attach
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            logger.error("Email credentials not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                            msg.attach(part)
                    else:
                        logger.warning(f"Attachment file not found: {file_path}")
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def send_report(
        self,
        recipient: str,
        report_type: str,
        report_data: str,
        attachment_path: Optional[str] = None
    ) -> bool:
        """
        Send a financial report email.
        
        Args:
            recipient: Email address of the recipient
            report_type: Type of report (e.g., "Daily", "Weekly", "Monthly")
            report_data: Report content
            attachment_path: Path to report file to attach
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        subject = f"Financial Report - {report_type}"
        body = f"""
        Financial Report - {report_type}
        
        {report_data}
        
        Please find the detailed report attached.
        """
        
        attachments = [attachment_path] if attachment_path else None
        return self.send_email(recipient, subject, body, attachments)
    
    def send_alert(
        self,
        recipient: str,
        alert_type: str,
        alert_message: str
    ) -> bool:
        """
        Send an alert email.
        
        Args:
            recipient: Email address of the recipient
            alert_type: Type of alert (e.g., "Anomaly", "Threshold", "Error")
            alert_message: Alert message content
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        subject = f"Financial Alert - {alert_type}"
        body = f"""
        Financial Alert - {alert_type}
        
        {alert_message}
        
        Please review this alert and take necessary action.
        """
        
        return self.send_email(recipient, subject, body) 