def generate_email(anomalies):
    n = len(anomalies)
    total = anomalies['amount'].sum()
    email = f"""
Subject: Aureus Fraud Alert - {n} Suspicious Transactions

Dear Founder/Investor,

Aureus has detected {n} suspicious transactions totaling ${total:,.2f} in your recent financial data. Please review the attached details and take necessary action.

Best regards,
Aureus AI Finance Assistant
"""
    return email
