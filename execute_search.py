import pandas_single_bedroom as psb
from user_information import SelectionKeys as sk
import send_gmail as sg

#simplify code in execute() 
class ContentFormat:
    def __init__(self, text, html):
        self.text = text
        self.html = html

    def write_mail(self):
        pass


#execute commands
def execute():
    psb.execute_search()
    data = psb.compile_dtfm()
    data_to_email = psb.find_rooms(data)

    data_send = sg.PrepEmail(data_to_email)
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
            html_body += f'I found a nice place in <u>{location.title()}</u> for you for <u>${price}</u> a month.<br>Posting: <a href="{url}">{title.title()}</a><br>'

        text, html = data_send.single_entry()
        text = text.format(body = text_body, name = name.title())
        html = html.format(body = html_body, name = name.title())
        send_email = sg.SendEmail(text, html)
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
        send_email = sg.SendEmail(text, html)
        send_email.process_shipment()
        print('Email sent.')
    else:
        print('No email sent.')
        pass

execute()