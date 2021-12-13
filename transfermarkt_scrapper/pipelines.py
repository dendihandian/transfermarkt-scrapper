# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class TransfermarktScrapperPipeline:
    def process_item(self, item, spider):
        return item

class SQLitePipeline:

    fields = [
        'player_id',
        'name',
        'position',
        'age',
        'national_1',
        'national_2',
        'left_club',
        'left_club_league',
        'left_club_country',
        'joined_club',
        'joined_club_league',
        'joined_club_country',
        'market_value',
        'market_value_p',
        'fee',
        'loan_fee',
        'loan_fee_p',
        'transfer_date',
        'transfer_date_p',
        'temp_dates_page',
        'temp_players_page',
        'transfer_date_p',
        'created_at',
        'updated_at'
    ]

    def open_spider(self, spider):
        self.connection = sqlite3.connect("data/transfermarkt.db")
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.process_item_transfers(item)
        return item

    def process_item_transfers(self, item):

        qms = ['?' for field in self.fields]
        # qms = ['?'] + qms

        values = [ item.get(field) for field in self.fields]
        # values = [None] + values

        self.cur.execute(f'''
            INSERT INTO transfers ({",".join(self.fields)}) VALUES ({",".join(qms)})
        ''', values)

        self.connection.commit()
