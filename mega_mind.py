import os
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup

# zillow detects driver and returns a captcha w/o credentials
REQUEST_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0',
    'Accept-Language': 'en-US',
}

# zillow results url -- application does not sign into and populate search form but relies on extant link
DESTINATION_WEDDING = os.environ['ENV_DEST_LINK']
FORM = os.environ['ENV_FORM_LINK']
DRIVER_PATH = os.environ['ENV_DRIVER_PATH']

# sleep time encourages element findability by driver (also looks more human)
TRY_TIME = 3.5


class EstateAgent:
    def __init__(self):
        self.credentials = REQUEST_HEADER
        self.neighborhood = DESTINATION_WEDDING
        self.paperwork = FORM
        self.upstart = webdriver.Chrome(DRIVER_PATH)
        
        # initialized with activated functions that in turn close out the driver once it's finished
        # remove/reassign these or add additional time.sleep to improve visibility
        self.leads = self.find_listings()
        self.submit_findings()

    def find_listings(self):
        leads = []
        response = requests.get(url=self.neighborhood, headers=self.credentials)
        response.raise_for_status()

        data = response.text

        # beautifulsoup scrapes and makes interactable the html 
        document = BeautifulSoup(data, 'html.parser')

        # articles are the interactable 'cards' that zillow serves up in results
        listings = document.find_all('article')

        for listing in listings:
            new_dictionary = {
                'address': listing.div.a.text,
                'rent': listing.div.div.next_sibling()[0].text,
                'link': listing.div.a.get('href')
            }

            leads.append(new_dictionary)
            
        # some results have rendant results deliniated with a '|' -- the more robust result is usually the latter
        # this tidies up such results, but is optional
        for entry in leads:
            a = entry['address']
            if '|' in a:
                b = a.split('| ')[1]
                entry['address'] = b

        return leads

    def submit_findings(self):

        driver = self.upstart
        leads = self.leads

        # instead of using sheety api to interact with google sheets, the below links to a simple premade google form
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
                
                # clicking through the submit field takes you to a refresh form option
                refresh_link = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
                refresh_link.click()
        finally:
            driver.close()




