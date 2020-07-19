import os
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from .paths import DATA_DIR


class emailMetaData:
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")
    receiver_email = "ira89@icloud.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Craigslist Housing"
    message["From"] = sender_email
    message["To"] = receiver_email


class Email:
    def __init__(self):
        self.text_body = ""
        self.html_body = ""

    def emailBody(self, location, price, bedroom, url, title):
        self.text_body += f"${price} a month in {location.title()}. ({bedroom} bedroom) {title.title()} ({url})"
        self.html_body += f'${price} a month in {location.title()}. ({bedroom} bedroom)<br><a href="{url}">{title.title()}</a><br>'

    def emailMarkup(self):
        text_markup = f"""\
            {self.text_body}
        """
        html_markup = f"""\
            <html>
            <body>
                <p>
                {self.html_body}<br>
                </p>
            </body>
            </html>
        """

        return text_markup, html_markup


def parse_unique_dtfm(emailObj):
    unique_dtfm = pd.read_csv(os.path.join(DATA_DIR, "new_peninsula_housing.csv"))
    if unique_dtfm.shape[0] == 0:
        return

    for _, post in unique_dtfm.iterrows():
        location = post["location"]
        price = "%.0f" % post["price"]
        bedroom = post["bedrooms"]
        url = post["url"]
        title = post["title"]

        emailObj.emailBody(location, price, bedroom, url, title)

    return emailObj


def send_email(metadata, text, html):
    text_mail = MIMEText(text, "plain")
    html_mail = MIMEText(html, "html")
    message = metadata.message

    message.attach(text_mail)
    message.attach(html_mail)

    ssl_context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as server:
        server.login(metadata.sender_email, metadata.sender_password)
        server.sendmail(
            metadata.sender_email, metadata.receiver_email, message.as_string()
        )


def write():
    metadata = emailMetaData
    email_body = parse_unique_dtfm(Email())
    try:
        text, html = email_body.emailMarkup()  # may return None - catch below
        send_email(metadata, text, html)
    except AttributeError:
        pass
