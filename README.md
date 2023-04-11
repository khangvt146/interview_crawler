# PYTHON SCRAPY SCRAPER
Amazon and Wayfair web-crawler using **Python Scrapy** and **Selenium**

* `amazon_crawler`: Scrapy Amazon Crawler (Using for Exercise 1 & Exercise 2)
* `wayfair`: Scrapy Wayfair Crawler (Using for Exercise 3)

## Install necessary libraries
Create virtual environment and running following command:
```
pip install -r requirements.txt
```

## Start MongoDB for saving crawl data
Replace your MongoDB username and password in compose file:
* `MONGO_INITDB_ROOT_USERNAME=<username>`
* `MONGO_INITDB_ROOT_PASSWORD=<password>`

Run compose file to create MongoDB container
```
docker-compose.yml up -d --build
```

## Using Amazon Spider
Run following code to start Amazon Spider:

```
cd amazon_crawler
scrapy crawl exercise_1_spider
scrapy crawl exercise_2_spider
```

* `exercise_1_spider`: spider uses for Exercise 1
* `exercise_2_spider`: spider uses for Exercise 2

Crawling results will be saved to `amazon_crawler/output` and correspond MongoDB collection

## Using Wayfair Spider
Run following code to start Wayfair Spider:

```
cd wayfair
scrapy crawl exercise_3_spider
```

* `exercise_3_spider`: spider uses for Exercise 3

Crawling results will be saved to `wayfair/output` and correspond MongoDB collection