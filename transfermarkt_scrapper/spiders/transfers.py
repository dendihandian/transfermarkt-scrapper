from dateutil.parser import parse
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

    latest_date = '2021-09-15'
    oldest_date = '2021-09-12'

    def start_requests(self):
        yield SplashRequest(url="https://www.transfermarkt.com/statistik/transfertage", callback=self.parse_transfers_pages, endpoint="execute", args={'lua_source': self.script, 'wait': 1})

    def parse_transfers_pages(self, response):

        latest_date = parse(self.latest_date)
        oldest_date = parse(self.oldest_date)

        dates = response.xpath("//table[@class='items']/tbody/tr")
        for date in dates:
            transfer_date = date.xpath("./td[1]/a/text()").get()
            date_link = date.xpath("./td[1]/a/@href").get()
            transfer_count = date.xpath("./td[2]/a/text()").get()

            transfer_date_parsed = parse(transfer_date)

            if (transfer_date_parsed >= oldest_date and transfer_date_parsed <= latest_date and int(transfer_count) > 0):

                yield SplashRequest(
                    url=self.base_url + date_link + '/plus/1', 
                    callback=self.parse_transfers_date_page,
                    cb_kwargs={'transfer_date': transfer_date}, 
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

        next_page_path = response.xpath("//li[@class='naechste-seite'][1]/a/@href").get()
        if (next_page_path):
            yield SplashRequest(
                url=self.base_url + next_page_path,
                callback=self.parse_transfers_date_page,
                cb_kwargs={'transfer_date': transfer_date},
                endpoint="execute",
                args={'lua_source': self.script, 'wait': 1}
            )


"""
poetry run scrapy crawl transfers
poetry run scrapy crawl transfers -o datasets/transfers/transfers.json
poetry run scrapy crawl transfers -o datasets/transfers/transfers.jl
"""
