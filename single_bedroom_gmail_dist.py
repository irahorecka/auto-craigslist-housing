#2019-08-25 Send emails with hyperlink for good deals found on craigslist housing.
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas_single_bedroom as psb


sender_email = "ira.python@gmail.com"
receiver_email = "ira89@icloud.com"
#password = input("Type your password and press enter:")
password = input('Gmail password: ')

message = MIMEMultipart("alternative")
message["Subject"] = "Craigslist Findings"
message["From"] = sender_email
message["To"] = receiver_email

#slight bug in creating updated file, i.e. data_to_email - revise this
data = psb.compile_dtfm()
data_to_email = psb.find_rooms(data)

if len(data_to_email) != 0:
    for index,row in data_to_email.iterrows():
        name = 'robert'
        location = row['Location']
        price = '%.0f' % row['Price']
        url = row['URL']
        title = row['Title']

        # Create the plain-text and HTML version of your message
        text = """\
        Hi {name},
        I found a nice place in {location} for you for ${price} a month.
        Check this out and let me know if you like it!
        {url}
        See you again,
        Ira"""
        html = """\
        <html>
        <body>
            <p>Hi {name},<br><br>
            I found a nice place in {location} for you for ${price} a month.<br>
            Check posting
            <a href="{url}">{title}</a> 
            and let me know if you like it!<br><br>
            See you again,<br>
            Ira
            </p>
        </body>
        </html>
        """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text.format(name = name.title(), location = location.title(), price = price, url = url), "plain")
    part2 = MIMEText(html.format(name = name.title(), location = location.title(), price = price, url = url, title = title), "html")

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
else:
    print('No email sent.')
    pass