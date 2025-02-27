import smtplib
from email.mime.text import MIMEText

from app.models.tokens import Token
from app.models.users import User

from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import pyotp
import os

load_dotenv()

class EmailRouter:
    def __init__(self, recipient):
        if not recipient:
            raise ValueError("Recipient is required")
        self.host = os.environ.get("EMAIL_HOST")
        self.port = os.environ.get("EMAIL_PORT")
        self.sender = os.environ.get("EMAIL_USER")
        self.password = os.environ.get("EMAIL_PASSWORD")
        self.recipient = recipient

    def send_otp(self, user:User):
        otp = pyotp.TOTP(os.environ.get("OTP_SECRET")).now()
        otp = otp.now()
        msg = MIMEMultipart()

        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = "OTP for your account"

        body = f"Dear {user.full_name.split(' ')[0]},\n\nYour OTP is {otp}. Please do not share this with anyone."
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.recipient, msg.as_string())
            server.quit()
        except Exception as e:
            print(e)
            return None
        return otp
    
    def send_verfication_confirmation(self, user:User):
        msg = MIMEMultipart()

        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = "Account verification"

        body = f"Dear {user.full_name.split(' ')[0]},\n\nYour account has been successfully verified."
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.recipient, msg.as_string())
            server.quit()
        except Exception as e:
            print(e)
            return False
        return True