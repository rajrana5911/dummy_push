from bs4 import BeautifulSoup
import scrapy
import subprocess
import os 

current_working_file = __file__

print(current_working_file)

class ExampleSpider(scrapy.Spider):
    name = "lyricsila"
    start_urls = ['https://www.groovypost.com/reviews/8-online-tools-draw-diagrams-flowcharts/']

    def parse(self, response):
        try:
            title = response.css('#post-header > h1 ::text').get()
        except:
            print("Title xpath is not proper")
            title = None
        try:
            content = response.css('#content-area > div').get()
        except:
            print("Content xpath is not proper")
            content = None
        try:
            feature_image = response.xpath('/html/body/div[1]/main/div[3]/div/div/section/div/div[1]/article/div/div[1]/div/div/div/div/div[1]/div/div[2]/picture/img/@src').getall()
        except:
            print("Feature image xpath is not proper")
            feature_image = None
        try:
            category = response.xpath('/html/body/div[6]/div[2]/div/div/article/div/div/div[2]/div/div[1]/div/div[8]/div').get()
        except:
            print("Category xpath is not proper")
            category = None
        try:
            date12 = response.xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/article/div/div/div[2]/header/div[3]/span/time/@datetime').get()
        except:
            print("date12 xpath is not proper")
            date12 = None
        
        yield {
            'content': content,
            'feature_image': feature_image,
            # 'category': category,
            'title': title,
            # 'date12':date12
            
        }
            
if __name__ == '__main__':
    process = subprocess.call(['scrapy', 'runspider', current_working_file])
