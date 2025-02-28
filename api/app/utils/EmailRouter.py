import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import pyotp
import os

from app.models.users import User

load_dotenv()

class EmailRouter:
    def __init__(self, recipient):
        if not recipient:
            raise ValueError("Recipient is required")
        self.host = os.environ.get("EMAIL_HOST")
        self.port = int(os.environ.get("EMAIL_PORT", 587))  # Ensure port is an integer, default to 587 if missing
        self.sender = os.environ.get("EMAIL_USER")
        self.password = os.environ.get("EMAIL_PASSWORD")
        self.recipient = recipient

    def send_otp(self, user: User):
        otp = pyotp.TOTP(os.environ.get("OTP_SECRET_KEY")).now()  # Fixed OTP generation issue
        
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = "OTP for your account"

        body = f"Dear Applicant,\n\nYour OTP is {otp}. Please do not share this with anyone."
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.recipient, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Error sending OTP email: {e}")  # Improved error logging
            return None
        return otp
    
    def send_verification_confirmation(self, user: User):  # Fixed method name typo
        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = "Account verification"

        body = f"Dear Applicant,\n\nYour account has been successfully verified."
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.recipient, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Error sending verification email: {e}")  # Improved error logging
            return False
        return True
