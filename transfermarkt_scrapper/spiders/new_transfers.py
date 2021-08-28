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
        print(response.body)

"""
poetry run scrapy crawl new_transfers
poetry run scrapy crawl new_transfers -o datasets/new_transfers.json
"""