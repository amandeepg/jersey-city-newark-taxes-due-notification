import urllib.request
from html_table_parser import HTMLTableParser
from datetime import date
from datetime import datetime
import os
import sendgrid
from sendgrid.helpers.mail import *
from bs4 import BeautifulSoup

ACCOUNT_NUMBER = os.environ.get('ACCOUNT_NUMBER')
DAYS_THRESHOLD = int(os.environ.get('DAYS_THRESHOLD', '31'))
FROM_EMAIL = os.environ.get('FROM_EMAIL')
TO_EMAIL = os.environ.get('TO_EMAIL')
EMAIL_SUBJECT = os.environ.get('EMAIL_SUBJECT')
SG = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API'))

def sentence_case(str):
    return '. '.join(i.capitalize() for i in str.split('. '))

def url_get_table(url):
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    p = HTMLTableParser()
    p.feed(f.read().decode('utf-8'))
    return p.tables

# print("\n\nPANDAS DATAFRAME\n")
# import pandas
# print(pandas.DataFrame(tables[0]))
# print("\n\nPANDAS DATAFRAME END\n")

def check(event, context):
    TODAY = date.today()
    tables = url_get_table(f'http://taxes.cityofjerseycity.com/ViewPay?accountNumber={ACCOUNT_NUMBER}')

    output = ''
    for line in reversed(tables[0]):
        due_date = line[2]
        description = sentence_case(line[3])
        open_balance = line[6]
        open_balance_dollars = 0.0
        try:
            open_balance_dollars = float(open_balance[1:].replace(',', ''))
        except ValueError:
            pass

        if open_balance_dollars > 0.0:
            days_diff = (datetime.strptime(due_date, '%m/%d/%Y').date() - TODAY).days
            if days_diff < DAYS_THRESHOLD:
                output += f'<u>{description}</u> of <u>{open_balance}</u> due on <u>{due_date}</u><br/>\n'

    if len(output) > 0:
        html_content = HtmlContent(output)
        plain_text = BeautifulSoup(html_text).get_text()
        plain_text_content = Content("text/plain", plain_text)

        print(plain_text)

        SG.send(message=Mail(Email(FROM_EMAIL), To(TO_EMAIL), EMAIL_SUBJECT, plain_text_content, html_content))

    return output
