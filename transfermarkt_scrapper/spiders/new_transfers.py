import scrapy


class NewTransfersSpider(scrapy.Spider):
    name = 'new_transfers'
    allowed_domains = ['transfermarkt.com']
    start_urls = ['https://www.transfermarkt.com/transfers/neuestetransfers/statistik?land_id=0&wettbewerb_id=alle&minMarktwert=500000&maxMarktwert=200000000&plus=1']

    def parse(self, response):
        for i in range(1,10):
            yield {
                'name': 'Placeholder'
            }
        # for transfer in response.css('table.items tbody tr'):
        #     yield {
        #         'name': 'Placeholder'
        #     }

# poetry run scrapy crawl new_transfers -o results/new_transfers.json