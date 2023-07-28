from ntpath import join
import scrapy
from datetime import datetime,timedelta
from urllib.parse import urlparse
import os
import csv
import mysql.connector


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    #FilePath="D:\\work\\python\\webscrape\\"
    mydb = mysql.connector.connect(
            host="3.140.57.116",
  user="wp_raj1",
  password="rajPassword95$",
  database="url_automation")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bulk_quill_bank where content is null and bqt_id = 73")
    myresult = mycursor.fetchall()
    #read url csv file
    #urlCsvFile = open(join(FilePath,"sitemapurl.csv"))
    #csvreader = csv.reader(urlCsvFile)
    rows = []
    #for row in csvreader:
    #    rows.append(row)
        #print(row)
    #urlCsvFile.close()
    def start_requests(self):
        #urls = [
        #    'https://www.hitc.com/feed/',
        #    'https://dmerharyana.org/feed/'
        #]
        #urls=self.rows
        for url in self.myresult:
            # print(url)
            yield scrapy.Request(url=url[1], meta={'bqt_id':url[6],'wcid':url[0]}, callback=self.parse)

    def parse(self, response):
        # print(response.status,"=========",response.url)
        
        # if response.status not in [200, 201]:
        #     print(response.status,"=========")
        domain = urlparse(response.url).netloc
        #print(response.xpath('//h1[@class="tdb-title-text"]').get())
        #print(response.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " td-post-content ")]').get(default='not-found'))
        self.mycursor.execute("SELECT * FROM bulk_quill_template where bqt_id=73")
        myresult = self.mycursor.fetchone()
        if not myresult:
          exit
        try:
            webTitle= response.css(myresult[2]).get() 
        except:
            webTitle=response.xpath(myresult[2]).get()
        # print(webTitle)
#        categoryy=response.xpath(myresult[5]).get()
        try:

            content=response.css(myresult[3]).get()
        except:
            content=response.xpath(myresult[3]).get()
        # try:
            
        #     image_link= response.css(myresult[4]).get()
        # except:
        #     image_link= "https://techraptor.net" +  response.xpath(myresult[4]).get()
        #data = [webTitle, content]

        mycursor = self.mydb.cursor()
#        sql = "update bulk_quill_bank set title=%s,content=%s,featured_image=%s,Category=%s where wcid=%s"
        sql = "update bulk_quill_bank set title=%s,content=%s where wcid=%s"

        # sql = "update bulk_quill_bank set content=%s where wcid=%s"
        val = (webTitle,content,response.meta['wcid'])

 #       val = (webTitle,content,image_link,categoryy,response.meta['wcid'])
        # val = (content,response.meta['wcid'])
        mycursor.execute(sql, val)
        self.mydb.commit()
        #with open('WebsiteContent.csv', 'w', encoding='UTF8', newline='') as f:
            #writer = csv.writer(f)
            # write the data
            #writer.writerow(data)
    #def closed(self, reason):
    #    ft = open(self.FilePathName, "w", encoding='utf-8')
    #    ft.write(self.LatestDate.strftime("%Y-%m-%d %H:%M:%S"))
    #    ft.close()