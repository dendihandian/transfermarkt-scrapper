import scrapy


class NewTransfersSpider(scrapy.Spider):
    name = 'new_transfers'
    allowed_domains = ['transfermarkt.com']
    start_urls = ['http://transfermarkt.com/']

    def parse(self, response):
        pass
