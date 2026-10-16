import os
import smtplib
from email.message import EmailMessage
from urllib.parse import quote


def send_verification_email(recipient: str, token: str) -> None:
    host = os.getenv("SMTP_HOST")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    if not host:
        raise RuntimeError("SMTP email service is not configured")

    port = int(os.getenv("SMTP_PORT", "587"))
    sender = os.getenv("FROM_EMAIL", username or "")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    verification_url = f"{frontend_url}/verify-email?token={quote(token)}"

    message = EmailMessage()
    message["Subject"] = "Verify your ServerWatch email"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(
        "Verify your ServerWatch account by opening this link:\n\n"
        f"{verification_url}\n\n"
        "This link expires in 24 hours."
    )

    with smtplib.SMTP(host, port, timeout=10) as smtp:
        if os.getenv("SMTP_TLS", "true").lower() == "true":
            smtp.starttls()
        if username and password:
            smtp.login(username, password)
        smtp.send_message(message)
