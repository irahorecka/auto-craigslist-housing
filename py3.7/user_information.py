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
    #note! with zipcode, selected_reg and state_keys will be empty
    state_keys = ['illinois']#['california']
    selected_reg = ['chicago']#['sfbay']
    selected_cat = ['apa']
    district_list = []#['oakland','berkeley','richmond','el cerrito','san leandro','alameda','albany','hercules']
    dist_filters = [60626, 5] #[zipcode, miles from zip]
    value_key = 0 #0 for statistically cheaper, 1 for statistically expensive 
    sd_val = 0.8
    name = 'ira'