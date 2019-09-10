import pandas_single_bedroom as psb
from user_information import SelectionKeys as sk
import send_gmail as sg

#simplify code in execute() 
class ContentFormat:
    def __init__(self, text, html):
        self.text = text
        self.html = html

    def single(self, location, price, url, title):
        self.text += f'I found a nice place in {location.title()} for you for ${price} a month.{url}'
        self.html += f'I found a nice place in <u>{location.title()}</u> for you for <u>${price}</u> a month.<br>Posting: <a href="{url}">{title.title()}</a><br>'

    def multiple(self, location, price, url, title, numbering):
        self.text += f'{numbering}) In {location.title()} for ${price} a month. {url}\n'
        self.html += f'{numbering}) In {location.title()} for ${price} a month.<br>Posting: <a href="{url}">{title.title()}</a><br>'

    def return_content(self):
        return self.text, self.html

#execute commands
def execute():
    psb.execute_search()
    data = psb.compile_dtfm()
    data_to_email = psb.find_rooms(data)

    data_send = sg.PrepEmail(data_to_email)
    content = ContentFormat("","")
    name = sk.name
    numbering = 1
    if len(data_to_email) == 0:
        print('No email sent.')
        pass
    elif len(data_to_email) == 1:
        location = data_to_email['Location']
        price = '%.0f' % data_to_email['Price']
        url = data_to_email['URL']
        title = data_to_email['Title']
        content.single(location, price, url, title)
        text, html = data_send.single_entry()
    else:
        for index,row in data_to_email.iterrows():
            location = row['Location']
            price = '%.0f' % row['Price']
            url = row['URL']
            title = row['Title']
            content.multiple(location, price, url, title, numbering)
            numbering += 1
        text_body, html_body = content.return_content()
        text, html = data_send.multiple_entry()
    text = text.format(body = text_body, name = name.title())
    html = html.format(body = html_body, name = name.title())
    send_email = sg.SendEmail(text, html)
    send_email.process_shipment()
    print('No email sent.')

execute()