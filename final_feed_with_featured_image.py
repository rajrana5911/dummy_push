from ntpath import join
import scrapy
from datetime import datetime,timedelta
from urllib.parse import urlparse
import os
import csv
import mysql.connector
import sys
import subprocess
current_working_file = __file__

import logging
current_working_folder = (os.path.realpath(os.path.dirname(__file__)))
# print(current_working_folder)
logging.basicConfig(filename=f'{current_working_folder}\error.log', level=logging.ERROR)

class QuotesSpider(scrapy.Spider):
    mydb = mysql.connector.connect(
    host="3.140.57.116",
    user="wp_raj1",
    password="rajPassword95$",
    database="automation00"
    )
    name = "quotes"
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM last_feed_date where category='feed' limit 1")
    myresult = mycursor.fetchone()
    if not myresult:
        sql = "insert into last_feed_date(last_update,category) values(now(),'feed')"
        mycursor.execute(sql)
        mycursor.execute("SELECT now();")
        currentdate = mycursor.fetchone()
        SavedDate = currentdate[0]
    else:
        SavedDate=myresult[1]

    LatestDate = datetime.now()#- timedelta(hours=5,minutes=30)#datetime.strptime(response.xpath('//pubDate/text()').get().replace(" +0000",""), '%a, %d %b %Y %H:%M:%S')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM destination_website where status = 1 ")
    myresult = mycursor.fetchall()
    # print(myresult)
    al_web=[]
    for ress in myresult:
#        print(ress[0])
        mycursor.execute("SELECT * FROM bulk_feed_website where des_id=(%s)" %  (ress[0]))

        websites = mycursor.fetchall()
        al_web.extend(websites)
    # print(al_web)
    def start_requests(self):
        print("request")
        for url in self.al_web:
 #           print(url)

            yield scrapy.Request(url=url[1], meta={'bfw_id':url[0],"Destination_id":url[6],"title12":url[2],"feature_imgg":url[4],"catego":url[5],'contte':url[3]}, callback=self.parse)

    def parse(self, response):
        print("parsing started")
        domain = urlparse(response.url).netloc
        response.selector.register_namespace('content','http://purl.org/rss/1.0/modules/content/')


        print(f'Saved Data:{self.SavedDate}')

        print(f'LatestDate Data:{self.LatestDate}')

        #File_object.close()
        for quote in response.xpath('//item'):
            pubDate=quote.xpath('.//pubDate/text()').get().replace(" +0000","") #Thu, 12 May 2022 17:43:01 +0000
            date_time_obj = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S')

            if self.SavedDate<date_time_obj:
                print(f'Pub Date: {date_time_obj}')
                title00 = quote.xpath('.//title/text()').get()
                content=quote.xpath('.//content:encoded/text()').get()
                print(content)
                category00 = quote.xpath('.//category/text()').get()
                # if response.meta['title12'] or response.meta['feature_imgg'] or response.meta['catego'] or response.meta['contte'] == 'NULL':
                url=quote.xpath('.//link/text()').get()
                bfwid=(response.meta['bfw_id'])
                dest_id=(response.meta['Destination_id'])
                #     title = quote.xpath('.//title/text()').get()
                #     content=quote.xpath('.//content:encoded/text()').get()
                #     category = quote.xpath('.//category/text()').get()
                    # print(title)
                    # print(category)
                    # print(response.meta['title12'])
                    # print(response.meta['feature_imgg'])
                    # print(response.meta['catego'])
                    # self.fea= response.meta['feature_imgg']
                    # self.cate= response.meta['catego']
                yield scrapy.Request(url=url,meta={'bfw_id':bfwid,"uurl":url,"Destination_id":dest_id,"title13":title00,"feature_imgg13":response.meta['feature_imgg'],"catego13":category00,"cantnt":response.meta['contte']}, callback=self.find_feature_image)
                
                # print(url)
        #         all_links.append(url)
        # # print(all_links)
        # for i in all_links:
        #     print(i)
                # sql = "insert into bulk_feed_content(bfw_id,url,Destination_id) values(%s,%s,%s)"
                # val = (response.meta['bfw_id'],self.url, response.meta['Destination_id'])
                # self.mycursor.execute(sql, val)
                # self.mydb.commit()
    def find_feature_image(self, response):
        aa=response.meta['title13']
        bb=response.meta['feature_imgg13']
        cc=response.meta['catego13']
        dd=response.meta['cantnt']
        urll=response.meta['uurl']
        bfwid1=(response.meta['bfw_id'])
        dest_id1=(response.meta['Destination_id'])
        
        # print(urll)
        # print("title ==",(response.xpath(f'{aa}').get()).strip())
        # print("feature_image ==",response.xpath(f'{bb}').get())
        # print("category == ",response.xpath(f'{cc}').get())
        try:
            sql = "insert into bulk_feed_content(bfw_id,url,title,content,featured_image,Category,Destination_id) values(%s,%s,%s,%s,%s,%s,%s)"
            val = (bfwid1,urll,aa,response.xpath(f'{dd}').get(),response.xpath(f'{bb}').get(),cc, dest_id1)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
        except Exception as e:
            logging.error(str(e))
        
        
    #self.log(f'Saved file {filename}')
    def closed(self, reason):
        sql = "update last_feed_date set last_update=now() where ldf_id=2"
        #print(str(self.myresult[0]))
        self.mycursor.execute(sql)
        self.mydb.commit() 
if __name__ == '__main__':
    process = subprocess.call(['scrapy', 'runspider', current_working_file])

