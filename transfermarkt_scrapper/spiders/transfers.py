from scrapy_splash import SplashRequest
import scrapy


class TransfersSpider(scrapy.Spider):
    name = 'transfers'
    allowed_domains = ['transfermarkt.com']
    base_url = 'https://www.transfermarkt.com'
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(2))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.transfermarkt.com/statistik/transfertage", callback=self.parse_transfers_pages, endpoint="execute", args={'lua_source': self.script, 'wait': 1})

    def parse_transfers_pages(self, response):
        dates = response.xpath("//table[@class='items']/tbody/tr")
        for date in dates:
            date_string = date.xpath("./td[1]/a/text()").get()
            date_link = date.xpath("./td[1]/a/@href").get()
            transfer_count = date.xpath("./td[2]/a/text()").get()
            # print(f"{date_string} - {transfer_count}")
            # print(f"{date_link}")

            yield SplashRequest(
                url=self.base_url + date_link, 
                callback=self.parse_transfers_date_page,
                cb_kwargs={'transfer_date': date_string}, 
                endpoint="execute", 
                args={'lua_source': self.script, 'wait': 1}
            )

    def parse_transfers_date_page(self, response, transfer_date):
        transfers = response.xpath("//table[@class='items']/tbody/tr")
        for transfer in transfers:
            name = transfer.xpath("./td[1]/table/tbody/tr[1]/td[2]/a/text()").get()
            yield {
                'name': name,
                'transfer_date': transfer_date
            }


"""
poetry run scrapy crawl transfers
poetry run scrapy crawl transfers -o datasets/transfers.json
poetry run scrapy crawl transfers -o datasets/transfers.jl
"""
