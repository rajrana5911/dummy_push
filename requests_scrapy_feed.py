import scrapy
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse
import os
import csv
import mysql.connector

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    mydb = mysql.connector.connect(
            host="3.140.57.116",
            user="wp_raj1",
            password="rajPassword95$",
            database="url_automation")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bulk_quill_bank where content is null and bqt_id = 70")
    myresult = mycursor.fetchall()
    rows = []

    def start_requests(self):
        for url in self.myresult:
            yield scrapy.Request(url=url[1], meta={'bqt_id': url[6], 'wcid': url[0]}, callback=self.parse)

    def parse(self, response):
        if response.status not in [200, 201]:
            print(response.status,"=========")
            # Status is not 200 or 201, fetch the data using requests library
            url = response.url
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to fetch data from URL: {url}. Error: {str(e)}")
                return

        domain = urlparse(response.url).netloc
        self.mycursor.execute("SELECT * FROM bulk_quill_template where bqt_id=70")
        myresult = self.mycursor.fetchone()
        if not myresult:
            exit
        try:
            webTitle = response.css(myresult[2]).get()
        except:
            webTitle = response.xpath(myresult[2]).get()
        
        try:
            content = response.css(myresult[3]).get()
        except:
            content = response.xpath(myresult[3]).get()
        
        try:
            image_link = response.css(myresult[4]).get()
        except:
            image_link = "https://techraptor.net" + response.xpath(myresult[4]).get()

        mycursor = self.mydb.cursor()
        sql = "update bulk_quill_bank set title=%s,content=%s,featured_image=%s where wcid=%s"
        val = (webTitle, content, image_link, response.meta['wcid'])
        mycursor.execute(sql, val)
        self.mydb.commit()
