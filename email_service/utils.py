from django.core.mail import EmailMessage
from email.utils import formatdate
import os
from datetime import datetime
import csv

from django.core.mail import send_mail

def save_email_to_csv(email, subject, from_email, to_email, date, message_id, body):
    directory = os.path.join("email_logs", email)
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, f"{email}.csv")

    # Check if file exists to write headers
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            # Write header row
            writer.writerow(["Subject", "From", "To", "Date", "Message-ID", "Body"])

        # Write email details
        writer.writerow([subject, from_email, to_email, date, message_id, body])

def send_email_to_user(to_email, subject, body):
    # Create the email object
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email="merchant@spfa.com",
        to=[to_email],
    )
    # Add any additional headers if needed
    email.extra_headers = {
        'X-Mailer': 'Django Email System',
        'Date': formatdate(localtime=True),  # Add a date header
    }
    # Send the email
    email.send()

    # Retrieve email headers for logging
    email_headers = {
        "Subject": email.subject,
        "From": email.from_email,
        "To": ", ".join(email.to),
        "Date": email.extra_headers['Date'],  # Include the date header
        "Message-ID": email.extra_headers.get('Message-ID', 'N/A')
    }
    return email_headers


def write_to_csv(email, transaction_data):
    """
    Write transaction data to a CSV file named after the email ID, inside the 'email_logs' folder.
    """
    # Specify the directory where the CSV files should be saved
    directory = os.path.join(os.getcwd(), 'email_logs')  # Absolute path to 'email_logs' folder

    # Ensure the directory exists; if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Path to the CSV file (inside 'email_logs' folder)
    file_path = os.path.join(directory, f"{email}.csv")

    file_exists = os.path.exists(file_path)
    
    # Open the file in append mode
    with open(file_path, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write headers only if the file is newly created
        if not file_exists:
            writer.writerow(["Transaction ID", "Amount", "Transaction Type", "Merchant", "Description", "Date"])
        
        # Write the transaction data
        writer.writerow([
            transaction_data['transaction_id'],
            transaction_data['amount'],
            transaction_data['transaction_type'],
            transaction_data['merchant'],
            transaction_data['description'],
            transaction_data['date']
        ])

def append_transaction_to_batch_csv(email, subject, body, amount, transaction_type, description):
    # Create the batch folder if it doesn't exist
    batch_folder = os.path.join("batch")
    os.makedirs(batch_folder, exist_ok=True)
    
    # File name based on today's date
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(batch_folder, f"{date_str}.csv")
    
    # Write or append the transaction details to the daily CSV
    is_new_file = not os.path.exists(file_path)
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the header if it's a new file
        if is_new_file:
            writer.writerow(["Email", "Subject", "Body", "Amount", "Transaction Type", "Description", "Timestamp"])
        
        # Append the transaction details
        writer.writerow([email, subject, body, amount, transaction_type, description, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])