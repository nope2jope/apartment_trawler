import os
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup

REQUEST_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0',
    'Accept-Language': 'en-US',
}

DESTINATION_WEDDING = os.environ['ENV_DEST_LINK']
FORM = os.environ['ENV_FORM_LINK']
DRIVER_PATH = os.environ['ENV_DRIVER_PATH']
TRY_TIME = 3.5


class EstateAgent:
    def __init__(self):
        self.credentials = REQUEST_HEADER
        self.neighborhood = DESTINATION_WEDDING
        self.paperwork = FORM
        self.upstart = webdriver.Chrome(DRIVER_PATH)
        self.leads = self.find_listings()
        self.submit_findings()

    def find_listings(self):
        leads = []
        response = requests.get(url=self.neighborhood, headers=self.credentials)
        response.raise_for_status()

        data = response.text

        document = BeautifulSoup(data, 'html.parser')

        listings = document.find_all('article')

        for listing in listings:
            new_dictionary = {
                'address': listing.div.a.text,
                'rent': listing.div.div.next_sibling()[0].text,
                'link': listing.div.a.get('href')
            }

            leads.append(new_dictionary)

        for entry in leads:
            a = entry['address']
            if '|' in a:
                b = a.split('| ')[1]
                entry['address'] = b

        return leads

    def submit_findings(self):

        driver = self.upstart
        leads = self.leads

        driver.get(self.paperwork)
        time.sleep(TRY_TIME)

        try:
            for lead in leads:
                address_input = driver.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
                rent_input = driver.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
                link_input = driver.find_element_by_xpath(
                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
                submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')

                address_input.click()
                address_input.send_keys(lead['address'])

                rent_input.click()
                rent_input.send_keys(lead['rent'])

                link_input.click()
                link_input.send_keys(lead['link'])

                time.sleep(TRY_TIME)

                submit_button.click()

                time.sleep(TRY_TIME)

                refresh_link = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
                refresh_link.click()
        finally:
            driver.close()




