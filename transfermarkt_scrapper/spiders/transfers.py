from dateutil.parser import parse
from scrapy_splash import SplashRequest
from datetime import datetime
import scrapy
import logging


class TransfersSpider(scrapy.Spider):
    name = 'transfers'
    allowed_domains = ['transfermarkt.com']
    base_url = 'https://www.transfermarkt.com'
    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(3))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    latest_date = '2021-05-10'
    oldest_date = '2021-05-01'
    transfer_pages_start = 10
    transfer_pages_end = 10

    def start_requests(self):
        starting_url = "https://www.transfermarkt.com/statistik/transfertage"

        if (self.transfer_pages_start):
            starting_url = starting_url + "?page=" + str(self.transfer_pages_start)

        logging.info('starting url...')

        yield SplashRequest(url=starting_url, callback=self.parse_transfers_pages, endpoint="execute", args={'lua_source': self.script, 'wait': 1}, cb_kwargs={'current_page': self.transfer_pages_start})

    def parse_transfers_pages(self, response, current_page):

        logging.info('parse_transfers_pages: ' + str(current_page))

        if current_page <= self.transfer_pages_end:

            latest_date = parse(self.latest_date)
            oldest_date = parse(self.oldest_date)

            dates = response.xpath("//table[@class='items']/tbody/tr")
            for date in dates:
                transfer_date = date.xpath("./td[1]/a/text()").get()
                date_link = date.xpath("./td[1]/a/@href").get()
                transfer_count = date.xpath("./td[2]/a/text()").get()

                transfer_date_parsed = parse(transfer_date)

                if (transfer_date_parsed >= oldest_date and transfer_date_parsed <= latest_date and int(transfer_count.replace('.', '')) > 0):

                    yield SplashRequest(
                        url=self.base_url + date_link + '/plus/1', 
                        callback=self.parse_transfers_date_page,
                        cb_kwargs={'transfer_date': transfer_date}, 
                        endpoint="execute", 
                        args={'lua_source': self.script, 'wait': 1}
                    )

            next_page_path = response.xpath("//li[@class='tm-pagination__list-item tm-pagination__list-item--icon-next-page'][1]/a/@href").get()
            if (next_page_path):
                yield SplashRequest(
                    url=self.base_url + next_page_path,
                    callback=self.parse_transfers_pages,
                    cb_kwargs={'current_page': current_page+1},
                    endpoint="execute",
                    args={'lua_source': self.script, 'wait': 1}
                )

    def parse_transfers_date_page(self, response, transfer_date):

        logging.info('parse_transfers_date_page: ' + str(transfer_date))

        transfer_date_parsed = parse(transfer_date).strftime('%Y-%m-%d')
        transfers = response.xpath("//table[@class='items']/tbody/tr")
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for transfer in transfers:

            href = transfer.xpath("./td[1]/table/tbody/tr[1]/td[2]/a[1]/@href").get()
            player_id = href.split("/").pop()

            name = transfer.xpath("./td[1]/table/tbody/tr[1]/td[2]/a[1]/text()").get()
            position = transfer.xpath("./td[1]/table/tbody/tr[2]/td/text()").get()
            age = transfer.xpath("./td[2]/text()").get()
            national_1 = transfer.xpath("./td[3]/img[1]/@title").get()
            national_2 = transfer.xpath("./td[3]/img[2]/@title").get()
            left_club = transfer.xpath("./td[4]/table/tbody/tr[1]/td[2]/a/text()").get()
            left_club_league = transfer.xpath("./td[4]/table/tbody/tr[2]/td[1]/a/text()").get()
            left_club_country = transfer.xpath("./td[4]/table/tbody/tr[2]/td[1]/img/@title").get()
            joined_club = transfer.xpath("./td[5]/table/tbody/tr[1]/td[2]/a/text()").get()
            joined_club_league = transfer.xpath("./td[5]/table/tbody/tr[2]/td[1]/a/text()").get()
            joined_club_country = transfer.xpath("./td[5]/table/tbody/tr[2]/td[1]/img/@title").get()
            market_value = transfer.xpath("./td[6]/text()").get()
            fee = transfer.xpath("./td[7]/a/text()").get()
            loan_fee = transfer.xpath("./td[7]/a/i[@class='normaler-text']/text()").get()

            yield {
                'player_id': player_id,
                'name': name,
                'position': position,
                'age': age,
                'national_1': national_1,
                'national_2': national_2,
                'left_club': left_club,
                'left_club_league': left_club_league,
                'left_club_country': left_club_country,
                'joined_club': joined_club,
                'joined_club_league': joined_club_league,
                'joined_club_country': joined_club_country,
                'market_value': market_value,
                'market_value_p': self.parse_value(market_value),
                'fee': fee,
                'loan_fee': loan_fee,
                'loan_fee_p': self.parse_value(loan_fee),
                'transfer_date': transfer_date,
                'transfer_date_p': transfer_date_parsed,
                'created_at': current_time,
                'updated_at': current_time
            }

        next_page_path = response.xpath("//li[@class='tm-pagination__list-item tm-pagination__list-item--icon-next-page']/a/@href").get()
        if (next_page_path):

            logging.info('into: ' + str(next_page_path))

            yield SplashRequest(
                url=self.base_url + next_page_path,
                callback=self.parse_transfers_date_page,
                cb_kwargs={'transfer_date': transfer_date},
                endpoint="execute",
                args={'lua_source': self.script, 'wait': 1}
            )

    def parse_value(self, value_string):
        if (value_string):
            value = value_string.replace('€', '')
            if ("Th." in value):
                value = value.replace("Th.", '')
                value = float(value) * 1000
            elif ("m" in value):
                value = value.replace("m", '')
                value = float(value) * 1000000
            else:
                value = value.replace("Th.", '').replace("m", '')

            return int(value)
        else:
            return None

"""
poetry run scrapy crawl transfers
poetry run scrapy crawl transfers --nolog
poetry run scrapy crawl transfers --loglevel INFO
poetry run scrapy crawl transfers --loglevel WARNING
poetry run scrapy crawl transfers -o datasets/transfers/transfers.json
poetry run scrapy crawl transfers -o datasets/transfers/transfers.jl
"""
