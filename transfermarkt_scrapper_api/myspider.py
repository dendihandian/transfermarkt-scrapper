import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://www.zyte.com/blog/']

    def parse(self, response):
        for title in response.css('.oxy-post-title'):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a.next'):
            yield response.follow(next_page, self.parse)

# poetry run scrapy runspider transfermarkt_scrapper_api\myspider.py
# poetry run scrapy runspider transfermarkt_scrapper_api\myspider.py -o results/blog.json