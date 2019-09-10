import pandas_single_bedroom as psb
from user_information import SelectionKeys as sk
import send_gmail as sg

#simplify code in execute() 
class ContentFormat:
    def __init__(self, text, html):
        self.text = text
        self.html = html

    def single(self, location, price, url, title):
        self.text += 'I found a nice place in {location.title()} for you for ${} a month.{}'.format(price,url)
        self.html += 'I found a nice place in {location.title()} for you for ${} a month.<br>Posting: <a href="{}">{title.title()}</a><br>'.format(price,url)

    def multiple(self, location, price, url, title, numbering):
        self.text += '{}) In {} for ${} a month. {}\n'.format(numbering,location.title(),price,url)
        self.html += '{}) In {} for ${} a month.<br>Posting: <a href="{}">{}</a><br>'.format(numbering,location.title(),price,url,title.title)

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
        return 'No email sent.'
    elif len(data_to_email) == 1:
        location = data_to_email['Location'][0]
        price = '%.0f' % data_to_email['Price'][0]
        url = data_to_email['URL'][0]
        title = data_to_email['Title'][0]
        content.single(location, price, url, title)
        text_body, html_body = content.return_content()
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
    return 'Email sent.'

print(execute())