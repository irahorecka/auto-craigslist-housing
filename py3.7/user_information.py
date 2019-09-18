#file to gather user information search criteria
from email.mime.multipart import MIMEMultipart

class UserInformation:
    sender_email = "ira.python@gmail.com"
    receiver_email = "ira89@icloud.com"
    password = input('Gmail password: ')

    message = MIMEMultipart("alternative")
    message["Subject"] = "Craigslist Findings"
    message["From"] = sender_email
    message["To"] = receiver_email

class SelectionKeys:
    #if we were solely looking at zip code... 
    state_keys = []#['california']
    selected_reg = []#['sfbay']
    selected_cat = ['apa']
    district_list = []#['oakland','berkeley','richmond','el cerrito','san leandro','alameda','albany','hercules']
    dist_filters = [94085, 5] #[zipcode, miles from zip]
    name = 'ira'