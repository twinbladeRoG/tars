import smtplib
from email.message import EmailMessage

from langchain.tools import tool

from src.core.logger import logger


@tool
def send_email(to: str, subject: str, body: str):
    """Send an email using SMTP"""
    msg = EmailMessage()
    msg["From"] = "no-reply@example.com"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    logger.debug(f"Sending mail to: '{to}'")

    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)

    return f"✅ Email sent to {to} via MailHog"
