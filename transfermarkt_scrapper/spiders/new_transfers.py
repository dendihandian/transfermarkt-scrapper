from scrapy import Spider
from scrapy_splash import SplashRequest

class NewTransfersSpider(Spider):
    name = 'new_transfers'
    allowed_domains = ['transfermarkt.com']
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.transfermarkt.com/transfers/neuestetransfers/statistik?land_id=0&wettbewerb_id=alle&minMarktwert=500000&maxMarktwert=200000000&plus=1", callback=self.parse, endpoint="execute", args={'lua_source': self.script})

    def parse(self, response):
        # print(response.body)

        transfers = response.xpath("//table[contains(@class, 'items')][1]/tbody/tr")
        for transfer in transfers:
            yield {
                'player_id': transfer.xpath("./td[1]/table/tbody/tr/td[2]/a/@id").get(),
                'name': transfer.xpath("./td[1]/table/tbody/tr/td[2]/a/text()").get(),
                'age': transfer.xpath("./td[2]/text()").get(),
                'position': transfer.xpath("./td[1]/table/tbody/tr[2]/td[1]/text()").get(),

                'left_club': transfer.xpath("./td[4]/table/tbody/tr[1]/td[2]/a/text()").get(),
                'left_club_league': transfer.xpath("./td[4]/table/tbody/tr[2]/td/a/text()").get(),
                'joined_club': transfer.xpath("./td[5]/table/tbody/tr[1]/td[2]/a/text()").get(),
                'joined_club_league': transfer.xpath("./td[5]/table/tbody/tr[2]/td/a/text()").get(),

                'transfer_date': transfer.xpath("./td[6]/text()").get(),
                'market_value': transfer.xpath("./td[7]/text()").get(),
                'fee': transfer.xpath("./td[8]/a/text()").get()
            }

"""
poetry run scrapy crawl new_transfers
poetry run scrapy crawl new_transfers -o datasets/new_transfers.json
"""