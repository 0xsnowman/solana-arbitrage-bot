import aiosmtplib
from email.mime.text import MIMEText
import random
from app.core.config import settings

verification_codes = {}

async def send_email(recipient: str):
    code = str(random.randint(100000, 999999))
    verification_codes[recipient] = code
    
    sender_email = settings.EMAIL_USER
    password = settings.EMAIL_PASSWORD

    print(sender_email)
    msg = MIMEText(f"Your verification code is: {code}")
    msg["Subject"] = "Your Verification Code"
    msg["From"] = sender_email
    msg["To"] = recipient

    await aiosmtplib.send(
        msg, hostname="smtp.gmail.com", port=587,
        username=sender_email, password=password, start_tls=True
    )

async def verify_code(email: str, user_code: str):
    return verification_codes.get(email) == user_code
