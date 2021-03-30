import os
import requests
from bs4 import BeautifulSoup

REQUEST_HEADER = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0',
    'Accept-Language': 'en-US',
}

FORM_LINK = os.environ['ENV_FORM']
DESTINATION_WEDDING = os.environ['ENV_FILTERED_RESULTS']

response = requests.get(url=DESTINATION_WEDDING, headers=REQUEST_HEADER)

data = response.text

document = BeautifulSoup(data, 'html.parser')

prices = document.findAll(name='div', class_='list-card-price')
links = document.findAll(name='a', class_='list-card-link list-card-link-top-margin')
addresses = document.findAll(name='address', class_='list-card-addr')

template = {
    'price': '',
    'url': '',
    'address':''
}

# now, why in god's name are there fewer links than prices or addresses?
counter = 1
for x in range(len(prices)):
    print(f'                              {counter}')
    print(prices[x].text)
    print(links[x].text)
    print(addresses[x].text)
    counter += 1




