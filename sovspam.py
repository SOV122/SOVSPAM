#!/usr/bin/env python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import csv
import os
import logging

logging.basicConfig(filename='sovspam.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

banner = """
  █████████     ███████    █████   █████  █████████  ███████████    █████████   ██████   ██████
 ███░░░░░███  ███░░░░░███ ░░███   ░░███  ███░░░░░███░░███░░░░░███  ███░░░░░███ ░░██████ ██████ 
░███    ░░░  ███     ░░███ ░███    ░███ ░███    ░░░  ░███    ░███ ░███    ░███  ░███░█████░███ 
░░█████████ ░███      ░███ ░███    ░███ ░░█████████  ░██████████  ░███████████  ░███░░███ ░███ 
 ░░░░░░░░███░███      ░███ ░░███   ███   ░░░░░░░░███ ░███░░░░░░   ░███░░░░░███  ░███ ░░░  ░███ 
 ███    ░███░░███     ███   ░░░█████░    ███    ░███ ░███         ░███    ░███  ░███      ░███ 
░░█████████  ░░░███████░      ░░███     ░░█████████  █████        █████   █████ █████     █████
 ░░░░░░░░░     ░░░░░░░         ░░░       ░░░░░░░░░  ░░░░░        ░░░░░   ░░░░░ ░░░░░     ░░░░░ 
"""

def send_email(smtp_server, smtp_port, username, password, recipient, subject, body, attachment=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        if attachment:
            with open(attachment, 'rb') as attach_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attach_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                msg.attach(part)
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            logging.info(f"Email sent to: {recipient}")
    except Exception as e:
        logging.error(f"Failed to send email to {recipient}: {e}")

def load_recipients(file_path):
    recipients = []
    try:
        with open(file_path, 'r') as file:
            if file_path.endswith('.csv'):
                reader = csv.reader(file)
                for row in reader:
                    recipients.append(row[0])
            else:
                for line in file:
                    recipients.append(line.strip())
    except Exception as e:
        logging.error(f"Error loading recipients: {e}")
    return recipients

def main():
    print(banner)
    print("Welcome to SOVSPAM!")
    
    smtp_server = input("Enter SMTP server: ")
    smtp_port = int(input("Enter SMTP port: "))
    username = input("Enter your email: ")
    password = input("Enter your password: ")
    
    subject = input("Enter email subject: ")
    body = input("Enter email body (HTML format supported): ")
    delay = float(input("Enter delay between emails (seconds): "))
    attachment = input("Enter file path for attachment (leave empty for no attachment): ") or None

    file_path = input("Enter recipients file path (CSV or TXT): ")
    recipients = load_recipients(file_path)

    for recipient in recipients:
        send_email(smtp_server, smtp_port, username, password, recipient, subject, body, attachment)
        time.sleep(delay)

if __name__ == "__main__":
    main()
