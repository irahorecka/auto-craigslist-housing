import smtplib, ssl
from email.mime.text import MIMEText
from user_information import UserInformation as ui

class PrepEmail:
    def __init__(self, dtfm):
        self.dtfm = dtfm

    def single_entry(self):
        text = """\
        Hi {name},

        {body}
        Good luck!
        - Ira"""
        html = """\
        <html>
        <body>
            <p>Hi {name},<br><br>
            {body}<br>
            Good luck!<br>
            - Ira
            </p>
        </body>
        </html>
        """
        return text, html

    def multiple_entry(self):
        text = """\
        Hi {name},

        {body}
        Good luck!
        - Ira"""
        html = """\
        <html>
        <body>
            <p>Hi {name},<br><br>
            I found some nice places for you:<br>
            {body}<br>
            Good luck!<br>
            - Ira
            </p>
        </body>
        </html>
        """
        return text, html


class SendEmail:
    def __init__(self, text, html):
        self.text = text
        self.html = html

    def process_shipment(self):
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(self.text, "plain")
        part2 = MIMEText(self.html, "html")
        message = ui.message

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(ui.sender_email, ui.password)
            server.sendmail(
                ui.sender_email, ui.receiver_email, message.as_string())