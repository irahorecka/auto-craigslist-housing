import os
from email.mime.multipart import MIMEMultipart

class UserInformation:
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")
    receiver_email = "ira89@icloud.com"
    

    message = MIMEMultipart("alternative")
    message["Subject"] = "Craigslist Housing"
    message["From"] = sender_email
    message["To"] = receiver_email