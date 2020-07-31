import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests


def write_email(new_posts, craigslist_param):
    """Main function to construct email sender, recipients,
    and content for new craigslist housing posts."""
    metadata = EmailMetadata()
    metadata.sender_email = craigslist_param.get("gmail_user")
    metadata.sender_password = craigslist_param.get("gmail_pass")
    metadata.receiver_email = craigslist_param.get("email_recipient")
    metadata.subject = craigslist_param.get("email_subject")
    metadata.construct_MIME()

    email_obj = parse_unique_dtfm(Email(), new_posts)
    try:
        text, html = email_obj.markup(
            craigslist_param.get("email_message")
        )  # may return None - catch below
        if text:  # make sure no empty str returned
            send_email(metadata, text, html)
    except AttributeError:
        pass


class EmailMetadata:
    """Constructor for email metadata."""

    def __init__(self):
        self.sender_email = ""
        self.sender_password = ""
        self.receiver_email = []
        self.subject = ""
        self.message = None

    def construct_MIME(self):
        """Construct MIMEMultipart object."""
        self.message = MIMEMultipart("alternative")
        self.message["Subject"] = self.subject
        self.message["From"] = self.sender_email
        self.message["To"] = ""  # to be populated downstream


class Email:
    """Construct email body from new posts."""

    def __init__(self):
        self.text_body = ""
        self.html_body = ""

    def body(self, location, price, bedroom, url, title):
        """Append post information to string template (text and html)."""
        self.text_body += f"${price} a month in {location.title()}. ({bedroom} bedroom) {title.title()} ({url})"
        self.html_body += f'${price} a month in {location.title()}. ({bedroom} bedroom)<br><a href="{url}">{title.title()}</a><br>'

    def markup(self, message):
        """Concatenate self.text_body and self.html_body in
        markup format for email."""
        text_markup = f"""\
            {self.text_body}
        """
        html_markup = f"""\
            <html>
            <body>
                <p>
                {message}
                </p>
                <p>
                {self.html_body}
                </p>
            </body>
            </html>
        """

        return text_markup, html_markup


def parse_unique_dtfm(email_obj, new_posts):
    """Retrieve relevant information from unique and new
    craigslist housing posts."""
    if new_posts.shape[0] == 0:
        return None

    for _, post in new_posts.iterrows():
        location = post["location"]
        price = "%.0f" % post["price"]
        bedroom = post["bedrooms"]
        url = post["url"]
        title = post["title"]

        if verify_invalid_post(url):
            continue
        email_obj.body(location, price, bedroom, url, title)

    return email_obj


def verify_invalid_post(url):
    """Ensure valid craigslist post prior to sending.
    Return True if invalid."""
    # TODO: boost with multithreading
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
        # TODO: send email in one batch, do not accumulate or persist
        for recipient in metadata.receiver_email:
            message["To"] = recipient
            server.sendmail(metadata.sender_email, recipient, message.as_string())
