from scrapy import Spider, Request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from wayfair.items import *

import datetime as dt
import json
import csv
import re
import time

from scrapy.utils.log import configure_logging 
import logging

class Exercise3Spider(Spider):
    name = "exercise_3_spider"
    allowed_domains = ["www.wayfair.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'wayfair.pipelines.WayfairBestSellerPipeline': 400
        }
    }
    
    def __init__(self, *args, **kwargs):
        """ Set path to geckodriver(Firefox) and set --headless for not displaying Firefox UI. """
        super(Exercise3Spider, self).__init__(*args, **kwargs)
        
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)

        PATH = "/geckodriver"
        
        firefox_options = Options()
        firefox_options.headless = True

        self.driver = webdriver.Firefox(executable_path=PATH, options=firefox_options)
        self.init_urls()
        self.other_urls = []

    def init_urls(self):
        self.start_urls = ['https://www.wayfair.com/furniture/sb0/sectionals-c413893.html']
            
    def parse(self, response):
        self.driver.get(response.url)
        print(self.driver.current_url)
        try:
            # body = '//*[@id="CardInstanceqSKez0utgAUwsB10_PE59A"]'
            body = '//*[@id="sbprodgrid"]/div[1]/div/div/div/div[48]'
            element_present = EC.presence_of_element_located((By.XPATH, body))
            WebDriverWait(self.driver, 30).until(element_present)
        except TimeoutException:
            self.logger.error("Time out waiting for page to fully render")
            return []
        
        prod_lst = []
        cnt = 0
        page = 1
        
        for item in self.driver.find_elements(By.XPATH, '//*[@id="sbprodgrid"]/div[1]/div/div/div/div/div/div/div/a'):
            product = WayfairProductDetail()       
            product.title = self._check_element_visible(item, './div[3]/h2')
            product.brand = self._check_element_visible(item, './p')
            
            new_price = self._check_element_visible(item, './div[4]/div/div')
            product.new_price = self._transform_new_price(new_price)
             
            product.last_price = self._check_element_visible(item, './div[4]/div/div/s')
            
            rating = self._check_element_visible(item, './div[5]/div/p')
            product.rating = self._transform_rating(rating)
            
            rating_count = self._check_element_visible(item, './div[5]/div/div[2]')
            if rating_count:
                product.rating_count = rating_count[1:-1]
            
            product.shipping_fee = self._check_element_visible(item, './div[6]/div/p')
            
            product.dtime = datetime.datetime.now().isoformat()
            
            try:
                sponsored = './div[7]/div[1]'
                WebDriverWait(item, 5).until(EC.presence_of_element_located((By.XPATH, sponsored)))
                product.sponsored = True
            except TimeoutException:
                product.sponsored = False
            
            cnt += 1
            time.sleep(1)
            prod_lst.append(product.to_json())
            
          
        # Save result to csv file
        with open("./output/exercise_3.csv", "a+") as output:
            fieldnames = ['title', 'brand', 'new_price', 'last_price', 'rating', 'rating_count', 'shipping_fee', 'sponsored', 'dtime']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            for item in prod_lst:
                writer.writerow({'title': item['title'], 'brand': item['brand'], 'new_price': item['new_price'], 'last_price': item['last_price'], 
                                'rating':item['rating'], 'rating_count':item['rating_count'], 'shipping_fee':item['shipping_fee'],
                                'sponsored':item['sponsored'], 'dtime':item['dtime']})
        
        # page += 1
        # if cnt < 100:
        #     new_url = 'https://www.wayfair.com/furniture/sb0/sofas-c413892.html'
        #     time.sleep(120)
        #     prod_lst.append(Request(new_url, self.parse))
        
        return prod_lst
    
    def _transform_rating(self, rating):
        rating_pattern = r"Rated ([\d\.]+|\d+) out of 5 stars"

        match = re.search(rating_pattern, rating)
        if match:
            rating = "Rated " + match.group(1) + " out of 5 stars"
            return rating
        else:
            return ""
        
    def _transform_new_price(self, new_price):
        pattern = r"\$[\d,]+.\d{2}"
        match = re.search(pattern, new_price)

        if match:
            price = match.group()
            return price
        else:
            return ''
        
    def _check_element_visible(self, driver, xpath):
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
            res = driver.find_element(By.XPATH, xpath).text
            return res
        except TimeoutException:
            return None
    
        