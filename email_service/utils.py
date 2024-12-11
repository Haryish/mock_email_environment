import aiosmtpd
from email.message import EmailMessage
import os
import csv
from datetime import datetime
import logging
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from datetime import datetime

# Path to store the email logs CSV
LOG_DIR = "email_logs"
BATCH_DIR = "batch"

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BATCH_DIR, exist_ok=True)

# Set up logging
logger = logging.getLogger(__name__)

def send_email_to_user(to_email, subject, body):
    try:
        email_message = EmailMessage(
            subject=subject,
            body=body,
            from_email="merchant@spfa.com",  # Your from email address
            to=[to_email]
        )
        email_message.content_subtype = "plain"  # Text email (not HTML)

        # Send the email
        email_message.send(fail_silently=False)

        # Add Date and Message-ID headers
        email_message['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        email_message['Message-ID'] = f"<{email_message['Date']}@{email_message['From']}>"

        logger.info(f"Email sent to {to_email} with subject: {subject}")
        return email_message

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return None


def write_to_csv(email, transaction_data):
    # Write transaction details to a daily CSV in batch folder
    batch_file_path = os.path.join(BATCH_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.csv")
    
    # Check if the CSV file exists, if not, create it with headers
    if not os.path.exists(batch_file_path):
        with open(batch_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=transaction_data.keys())
            writer.writeheader()
            writer.writerow(transaction_data)
    else:
        with open(batch_file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=transaction_data.keys())
            writer.writerow(transaction_data)
    
    # Now, log email details in email_logs folder
    email_log_file_path = os.path.join(LOG_DIR, f"{email}.csv")
    email_data = {
        "subject": transaction_data.get("subject"),
        "from": "merchant@spfa.com",
        "to": email,
        "date": transaction_data.get("date"),
        "message_id": f"<{datetime.now().timestamp()}@merchant.com>",
        "body": transaction_data.get("body")
    }

    # Check if the email log file exists, if not, create it with headers
    if not os.path.exists(email_log_file_path):
        with open(email_log_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=email_data.keys())
            writer.writeheader()
            writer.writerow(email_data)
    else:
        with open(email_log_file_path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=email_data.keys())
            writer.writerow(email_data)
