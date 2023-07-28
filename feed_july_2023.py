# First, install scrapy if you haven't already: pip install scrapy

import scrapy
import mysql.connector  # Assuming you are using MySQL for the database, you'll need to install 'mysql-connector-python': pip install mysql-connector-python

# Define a spider to crawl the data
class MySpider(scrapy.Spider):
    name = 'my_spider'

    def start_requests(self):
        # Replace 'your_database_info' with the actual database connection details
        mydb = mysql.connector.connect(
  host="3.140.57.116",
  user="wp_raj1",
  password="rajPassword95$",
  database="url_automation"
)
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM multiple_destination_websites where status = 1 ")
        myresult = mycursor.fetchall()
        listt=[]
        for des_id in myresult:
            listt.append(des_id[0])
        alll=[]

        for bfw_idd in listt:
            
            mycursor.execute("SELECT * FROM bulk_quill_template where bqt_id=(%s)" % (bfw_idd) )
            webs = mycursor.fetchall()
            alll.extend(webs)

        for bfw_i in alll:
            
            mycursor.execute("SELECT * FROM bulk_quill_bank where bqt_id=(%s) and status is Null " % (bfw_i) )
            webs = mycursor.fetchall()
            alll.extend(webs[0:2])

        for row in alll:
            
            url = row[0]
            title_selector = row[1]
            content_selector = row[2]
            image_selector = row[3]

            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={
                'title_selector': title_selector,
                'content_selector': content_selector,
                'image_selector': image_selector
            })

    def parse(self, response, title_selector, content_selector, image_selector):
        # Extract data using provided selectors
        title = response.css(title_selector).get()
        content = response.css(content_selector).get()
        image = response.css(image_selector).get()

        # Process the extracted data or save it to a file/database as needed
        # For now, we'll print it as an example
        print("Title:", title)
        print("Content:", content)
        print("Image:", image)


# To run the spider, you can use the scrapy command-line tool or run it programmatically
from scrapy.crawler import CrawlerProcess

# Replace 'settings' with any additional Scrapy settings you want to use
process = CrawlerProcess(settings={})
process.crawl(MySpider)
process.start()
