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

class Exercise2Spider(Spider):
    name = "exercise_2_spider"
    allowed_domains = ["www.amazon.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon_crawler.pipelines.AmazonProductDetailPipeline': 400
        }
    }
    
    def __init__(self, *args, **kwargs):
        """ Set path to geckodriver(Firefox) and set --headless for not displaying Firefox UI. """
        super(Exercise2Spider, self).__init__(*args, **kwargs)
        
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)

        PATH = "./amazon_crawler/geckodriver"
        
        firefox_options = Options()
        firefox_options.headless = True

        self.driver = webdriver.Firefox(executable_path=PATH, options=firefox_options)
        self.init_urls()
        self.other_urls = []

    def init_urls(self):
        asin_list = ["B07MFZXR1B", "B07CRG7BBH", "B07VS8QCXC"]

        self.start_urls = []
        for item in asin_list:
            url = "https://www.amazon.com/dp/{}".format(item)
            self.start_urls.append(url)
            
    def parse(self, response):
        self.driver.get(response.url)
        try:
            # body = '//*[@id="CardInstanceqSKez0utgAUwsB10_PE59A"]'
            body = '//*[@id="ppd"]'
            element_present = EC.presence_of_element_located((By.XPATH, body))
            WebDriverWait(self.driver, 10).until(element_present)
        except TimeoutException:
            self.logger.error("Time out waiting for page to load")
            return []
        
        # Parse web page information
        product = AmazonProductDetail()
        product.title = self.driver.find_element(By.XPATH, '//span[@id="productTitle"]').text
       
        new_price = '//*[@id="corePrice_feature_div"]/div/span/span[1]'
        product.new_price = self.driver.execute_script("return arguments[0].innerHTML", self.driver.find_element(By.XPATH, new_price))
       
        try:
            last_price = '//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span/span[2]'
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, last_price)))
            product.last_price = self.driver.execute_script("return arguments[0].innerHTML", self.driver.find_element(By.XPATH, last_price))
        except TimeoutException:
            pass
        
        rating = '(//*[@id="acrPopover"]/span[1]/a/i[1]/span)[1]'
        product.rating = self.driver.execute_script("return arguments[0].innerHTML", self.driver.find_element(By.XPATH, rating))
        
        product.rating_count = self.driver.find_element(By.XPATH, '(//*[@id="acrCustomerReviewText"])[1]').text
        
        img_url = '//*[@id="landingImage"]'
        product.main_img_url = self.driver.execute_script("return arguments[0].getAttribute('src')", self.driver.find_element(By.XPATH, img_url))
        
        product.dtime = datetime.datetime.now().isoformat()
        prod_obj = product.to_json()
                                
        # Save result to csv file
        with open("./output/exercise_2.csv", "a+") as output:
            fieldnames = ['title', 'new_price', 'last_price', 'rating', 'rating_count', 'main_img_url', 'dtime']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
                 
            writer.writerow({'title': prod_obj['title'], 'new_price': prod_obj['new_price'], 'last_price': prod_obj['last_price'], 
                             'rating': prod_obj['rating'], 'rating_count': prod_obj['rating_count'], 'main_img_url': prod_obj['main_img_url'],
                            'dtime': prod_obj['dtime']})
        
        return prod_obj
        
        
        