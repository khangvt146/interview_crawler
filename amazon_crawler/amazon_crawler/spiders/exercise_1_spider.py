from scrapy import Spider, Request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from amazon_crawler.items import *

import datetime as dt
import json
import csv

from scrapy.utils.log import configure_logging 
import logging

class Exercise1Spider(Spider):
    name = "exercise_1_spider"
    allowed_domains = ["www.amazon.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon_crawler.pipelines.AmazonBestSellerPipeline': 400
        }
    }
    
    def __init__(self, *args, **kwargs):
        """ Set path to geckodriver(Firefox) and set --headless for not displaying Firefox UI. """
        super(Exercise1Spider, self).__init__(*args, **kwargs)
        
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)

        PATH = "/geckodriver"
        
        firefox_options = Options()
        firefox_options.headless = True

        self.driver = webdriver.Firefox(executable_path=PATH, options=firefox_options)
        self.init_urls()
        self.other_urls = []

    def init_urls(self):
        category_list = ['16225007011', '172456', '193870011']
        self.start_urls = []
        for item in category_list:
            url = "https://www.amazon.com/gp/bestsellers/hi/{}".format(item)
            self.start_urls.append(url)
            
    def parse(self, response):
        self.driver.get(response.url)
        try:
            # body = '//*[@id="CardInstanceqSKez0utgAUwsB10_PE59A"]'
            body = '//*[@data-card-metrics-id="p13n-zg-list-grid-desktop_zeitgeist-lists_2"]'
            element_present = EC.presence_of_element_located((By.XPATH, body))
            WebDriverWait(self.driver, 10).until(element_present)
        except TimeoutException:
            self.logger.error("Time out waiting for page to load")
            return []
        
        prod_lst = []
        
        for item in self.driver.find_elements(By.XPATH, '//*[@id="gridItemRoot"]'):
            product = AmazonCrawlerItem()
            product.rank = item.find_element(By.XPATH, './div/div[1]').text
            product.name = item.find_element(By.XPATH, './div/div[2]/div/a[2]').text
            product.url =  item.find_element(By.XPATH, './div/div[2]/div/a[1]').get_attribute('href')
            product.price = item.find_element(By.XPATH, './div/div[2]/div/div[2]').text
            product.dtime = datetime.datetime.now().isoformat()
                        
            prod_lst.append(product.to_json())
        
        # Save result to csv file
        with open("./output/exercise_1.csv", "a+") as output:
            fieldnames = ['rank', 'name', 'price', 'url', 'dtime']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            for item in prod_lst:
                writer.writerow({'rank': item['rank'], 'name': item['name'], 'price': item['price'], 'url': item['url'], 'dtime':item['dtime']})
        
        return prod_lst
        
        
        