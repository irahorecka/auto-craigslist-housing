import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import utils


def write_email(new_posts, craigslist_param):
    """Main function to construct email sender, recipients,
    and content for new craigslist housing posts."""
    metadata = EmailMetadata()
    metadata.sender_email = craigslist_param.get("gmail_user")
    metadata.sender_password = craigslist_param.get("gmail_pass")
    metadata.receiver_email = craigslist_param.get("email_recipient")
    metadata.subject = craigslist_param.get("email_subject")
    metadata.construct_MIME()

    email_obj = add_new_posts(Email(craigslist_param.get("housing_type")), new_posts)
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

    def __init__(self, housing_type):
        self.housing_type = housing_type
        self.text_body = ""
        self.html_body = ""

    def body(self, location, price, bedrooms, url, title):
        """Append post information to string template (text and html)."""
        if self.housing_type == "roo":    
            self.text_body += f"${price} a month in {location.title()}. {title.title()} ({url})"
            self.html_body += f'${price} a month in {location.title()}.<br><a href="{url}">{title.title()}</a><br>'
        else:
            self.text_body += f"${price} a month in {location.title()}. ({bedrooms} bedroom) {title.title()} ({url})"
            self.html_body += f'${price} a month in {location.title()}. ({bedrooms} bedroom)<br><a href="{url}">{title.title()}</a><br>'

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


def add_new_posts(email_obj, new_posts_dtfm):
    """Add post attributes to email object if post is
    valid."""
    if new_posts_dtfm.shape[0] == 0:
        return None

    new_posts = [post for _, post in new_posts_dtfm.iterrows()]
    response = utils.map_threads(parse_verify_posts, new_posts)

    for post in response:
        if post is None:
            continue
        email_obj.body(
            post["location"],
            post["price"],
            post["bedrooms"],
            post["url"],
            post["title"],
        )

    return email_obj


def parse_verify_posts(post):
    """Parse posts to retrieve attributes and verify a valid
    url -- return None if invalid. This function works with
    the map_threads module from _threadings.py"""
    invalid_flag = "This posting has been flagged for removal."
    deleted_flag = "This posting has been deleted by its author."
    post_content = {"url": post["url"]}
    resp_content = requests.get(post_content["url"]).content.decode("utf-8")
    if any(flag in resp_content for flag in [invalid_flag, deleted_flag]):
        return None

    post_content["location"] = post["location"]
    post_content["price"] = "%.0f" % post["price"]
    post_content["bedrooms"] = post["bedrooms"]
    post_content["title"] = post["title"]

    return post_content


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
