import os
import smtplib
import ssl
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd


def write_email(new_posts):
    """Main function to construct email sender, recipients,
    and content for new craigslist housing posts."""
    metadata = EmailMetadata
    email_obj = parse_unique_dtfm(Email())
    try:
        text, html = email_obj.markup()  # may return None - catch below
        if text:  # make sure no empty str returned
            send_email(metadata, text, html)
    except AttributeError:
        pass


class EmailMetadata:
    """Constructor for email metadata."""

    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")
    receiver_email = ["ira89@icloud.com"]

    message = MIMEMultipart("alternative")
    message["Subject"] = "Craigslist Housing"
    message["From"] = sender_email
    message["To"] = ""  # to be populated in future


class Email:
    """Construct email body from new posts."""

    def __init__(self):
        self.text_body = ""
        self.html_body = ""

    def body(self, location, price, bedroom, url, title):
        self.text_body += f"${price} a month in {location.title()}. ({bedroom} bedroom) {title.title()} ({url})"
        self.html_body += f'${price} a month in {location.title()}. ({bedroom} bedroom)<br><a href="{url}">{title.title()}</a><br>'

    def markup(self):
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


def parse_unique_dtfm(emailObj, new_posts):
    """Retrieve relevant information from unique and new
    craigslist housing posts."""
    if new_posts.shape[0] == 0:
        return

    for _, post in new_posts.iterrows():
        location = post["location"]
        price = "%.0f" % post["price"]
        bedroom = post["bedrooms"]
        url = post["url"]
        title = post["title"]

        if verify_invalid_post(url):
            continue
        emailObj.body(location, price, bedroom, url, title)

    return emailObj


def verify_invalid_post(url):
    """Ensure valid craigslist post prior to sending.
    Return True if invalid."""
    post = requests.get(url).content.decode("utf-8")
    invalid_flag = "This posting has been flagged for removal."
    deleted_flag = "This posting has been deleted by its author."

    return any(flag in post for flag in [invalid_flag, deleted_flag])


def send_email(metadata, text, html):
    """Build and send email."""
    text_mail = MIMEText(text, "plain")
    html_mail = MIMEText(html, "html")
    message = metadata.message

    message.attach(text_mail)
    message.attach(html_mail)

    ssl_context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context) as server:
        server.login(metadata.sender_email, metadata.sender_password)
        for recipient in metadata.receiver_email:
            message["To"] = recipient
            server.sendmail(metadata.sender_email, recipient, message.as_string())
