import scrapy
import logging

class FlipkartSpider(scrapy.Spider):
    name = 'mobile' #name of spider
    start_urls = ["https://www.flipkart.com/mobiles-accessories/mobiles/pr?sid=tyy,4io"]

    def parse(self,response):
        self.logger.info('Url called in parse on %s', response.url)
        logging.log(logging.WARNING, 'inside parse')
        for products in response.css('div._13oc-S'):
            try:
                yield{
                    'name' : products.css('div._4rR01T::text').get(),
                    'price' : products.css('div._30jeq3._1_WHN1::text').get().replace('₹',''),
                    'link' : products.css('a._1fQZEK').attrib['href'],
                }
            except:
                yield{
                    'name' : products.css('div._4rR01T::text').get(),
                    'price' : 'Sold out',
                    'link' : products.css('a._1fQZEK').attrib['href'],
                }

        next_page = response.css('a._1LKTO3').attrib['href']

        next_links = response.css('a._1LKTO3')

        if next_page is not None and len(next_links)==1:
            yield response.follow(next_page, callback=self.parse)
        elif len(next_links)>1:
            for index, newlinks in enumerate(next_links):
                if index!=0:
                    logging.log(logging.WARNING, 'newlinkes here')
                    logging.log(logging.WARNING, newlinks.css('a._1LKTO3').attrib['href'])
                    yield response.follow(newlinks.css('a._1LKTO3').attrib['href'], callback=self.parse)