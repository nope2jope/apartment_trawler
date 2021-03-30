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

listings = document.find_all('article')
listed_listings = []

for listing in listings:
    new_dictionary = {
        'address': listing.div.a.text,
        'rent': listing.div.div.next_sibling()[0].text,
        'link': listing.div.a.get('href')
    }

    listed_listings.append(new_dictionary)

for i in listed_listings:
    print(i)



