#2019-08-25 Send emails with hyperlink for good deals found on craigslist housing.
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas_single_bedroom as psb
import selection_key as sk

sender_email = "ira.python@gmail.com"
receiver_email = "ira89@icloud.com"
password = input('Gmail password: ')

message = MIMEMultipart("alternative")
message["Subject"] = "Craigslist Findings"
message["From"] = sender_email
message["To"] = receiver_email

psb.execute_search()
data = psb.compile_dtfm()
data_to_email = psb.find_rooms(data)

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

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

data_send = PrepEmail(data_to_email)
text_body = ""
html_body = ""
name = sk.name
numbering = 1
if len(data_to_email) == 1:
    for index,row in data_to_email.iterrows():
        location = row['Location']
        price = '%.0f' % row['Price']
        url = row['URL']
        title = row['Title']

        text_body += f'I found a nice place in {location.title()} for you for ${price} a month.{url}'
        html_body += f'I found a nice place in {location.title()} for you for ${price} a month.<br>Posting: <a href="{url}">{title.title()}</a><br>'

    text, html = data_send.single_entry()
    text = text.format(body = text_body, name = name.title())
    html = html.format(body = html_body, name = name.title())
    send_email = SendEmail(text, html)
    send_email.process_shipment()
    print('Email sent.')
elif len(data_to_email) > 1:
    for index,row in data_to_email.iterrows():
        location = row['Location']
        price = '%.0f' % row['Price']
        url = row['URL']
        title = row['Title']

        text_body += f'{numbering}) In {location.title()} for ${price} a month. {url}\n'
        html_body += f'{numbering}) In {location.title()} for ${price} a month.<br>Posting: <a href="{url}">{title.title()}</a><br>'
        numbering += 1
    text, html = data_send.multiple_entry()
    text = text.format(body = text_body, name = name.title())
    html = html.format(body = html_body, name = name.title())
    send_email = SendEmail(text, html)
    send_email.process_shipment()
    print('Email sent.')
else:
    print('No email sent.')
    pass