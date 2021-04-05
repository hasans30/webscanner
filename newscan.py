import requests
import os
import random
import time
import sys

from worklist import getRange
from bs4 import BeautifulSoup
url = 'https://egov.uscis.gov/casestatus/mycasestatus.do'
session = requests.Session()
oldContent = []


def getStatus(receiptNumber):
    headers = {'User-Agent': 'Mozilla/5.0'}
    payload = {'appReceiptNum': receiptNumber}
    response = session.post(url, headers=headers, data=payload)

    parsedContent = BeautifulSoup(response.text, 'html.parser')
    entries = parsedContent.find('div', {
                                 'class': 'col-lg-12 appointment-sec center'}).find('div', {'class': 'rows text-center'})
    status = entries.find('h1').getText()
    detail = entries.find('p').getText()
    content = receiptNumber+'\t'+status+'\t'+detail
    return content


def getIfUpdated(filename):
    try:
        with open(filename, encoding="utf-8", mode="r") as file:
            oldContent = file.readlines()
            file.close()
            return oldContent
    except Exception as e:
        print('exception occurred while reading file')
        print(e)


# tasks = ['LIN2190'+str(i) for i in range(235000, 245000)]
tasks = ["MSC2190356565", "MSC2190356554", "MSC2190356577"]

# remove already scanned items
status = ''
for i in tasks:
    try:
        status = getStatus(str(i))
    except Exception as ex:
        print(ex)
    print(status)
    # so that uscis don't consider throttle us.
    time.sleep(random.randint(2, 5))
