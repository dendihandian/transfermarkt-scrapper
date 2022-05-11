import scrapy


class TestSpiderSpider(scrapy.Spider):
    name = 'test_spider'
    allowed_domains = ['transfermarkt.com']
    start_urls = ['https://www.transfermarkt.com/statistik/transfertage/']

    def parse(self, response):
        pass


"""
poetry run scrapy crawl test_spider
poetry run scrapy crawl test_spider --nolog
poetry run scrapy crawl test_spider --loglevel INFO
poetry run scrapy crawl test_spider --loglevel WARNING
poetry run scrapy crawl test_spider -o data/test_spider/test_spider.json
poetry run scrapy crawl test_spider -o data/test_spider/test_spider.jl
"""

