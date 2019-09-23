import find_deals as fd
import cl_scraper as cs
from user_information import SelectionKeys as sk
import send_gmail as sg
import os
base_dir = os.getcwd()

class ContentFormat:
    def __init__(self, text, html):
        self.text = text
        self.html = html

    #determine if bedrooms could be incorporated in sending emails out for apt.
    def single(self, location, price, url, title, bedroom = " "):
        self.text += f'I found a nice{bedroom}place in {location.title()} for you for ${price} a month.{url}'
        self.html += f'I found a nice{bedroom}place in {location.title()} for you for ${price} a month.<br>Posting: <a href="{url}">{title.title()}</a><br>'

    def multiple(self, location, price, url, title, numbering, bedroom = "In"):
        self.text += f'{numbering}) {bedroom} {location.title()} for ${price} a month. {url}\n'
        self.html += f'{numbering}) {bedroom} {location.title()} for ${price} a month.<br>Posting: <a href="{url}">{title.title()}</a><br>'

    def return_content(self):
        return self.text, self.html

#execute commands
def execute():
    os.chdir(base_dir)
    search_criteria = cs.ExecSearch(sk.state_keys, sk.dist_filters, sk.selected_reg, sk.district_list, sk.selected_cat)
    search_criteria.cl_search()
    data = fd.compile_dtfm()
    data_to_email = fd.find_rooms(data, sk.sd_val, sk.value_key)
    os.chdir(base_dir)

    data_send = sg.PrepEmail(data_to_email)
    content = ContentFormat("","")
    name = sk.name
    numbering = 1
    if len(data_to_email) == 0:
        return 'No email sent.'
    elif len(data_to_email) == 1:
        location = data_to_email['Location'].iloc[0]
        price = '%.0f' % data_to_email['Price'].iloc[0]
        url = data_to_email['URL'].iloc[0]
        title = data_to_email['Title'].iloc[0]
        bedroom = data_to_email['Bedrooms'].iloc[0]
        if bedroom == 'None':
            content.single(location, price, url, title)
        else:
            content.single(location, price, url, title, f' {bedroom} bedroom ')
        text_body, html_body = content.return_content()
        text, html = data_send.single_entry()
    else:
        for index,row in data_to_email.iterrows():
            location = row['Location']
            price = '%.0f' % row['Price']
            url = row['URL']
            title = row['Title']
            bedroom = row['Bedrooms']
            if bedroom == 'None':
                content.multiple(location, price, url, title, numbering)
            else:
                content.multiple(location, price, url, title, numbering, f'{bedroom} bedroom place in')
            numbering += 1
        text_body, html_body = content.return_content()
        text, html = data_send.multiple_entry()
    text = text.format(body = text_body, name = name.title())
    html = html.format(body = html_body, name = name.title())
    send_email = sg.SendEmail(text, html)
    send_email.process_shipment()
    return 'Email sent.'

#print(execute())
