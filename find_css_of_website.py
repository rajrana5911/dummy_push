from bs4 import BeautifulSoup
import scrapy
import subprocess
import os 

current_working_file = __file__

print(current_working_file)

class ExampleSpider(scrapy.Spider):
    name = "lyricsila"
    start_urls = ['https://www.gadgetbridge.com/gadget-reviews/iqoo-z6-pro-5g-review-a-lot-of-hits-and-few-misses-right-buy-at-this-price/']

    def parse(self, response):
        
        try:
            url_of_article=response.css(' image-link media-ratio ratio-16-9 ::attr(href)').getall()
            # url_of_article=response.css(' #container > section > div > section:nth-child(2) > div ::attr(href)').getall()

        except:
            print("url_of_article css is not proper")
            url_of_article = None
        try:
            feat=response.css('.entry-thumb::attr(src)) ').get()

        except:
            print("feat css is not proper")
            feat = None
        yield {
            'url_of_article':url_of_article,
            'feat':feat
            
        }
            
if __name__ == '__main__':
    process = subprocess.call(['scrapy', 'runspider', current_working_file])
