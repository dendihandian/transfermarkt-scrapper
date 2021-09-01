import os
from datetime import datetime

filename = datetime.today().strftime("%Y_%m_%d_%H_%M_%S") + '.jl'
os.system(f"poetry run scrapy crawl new_transfers -o datasets/new_transfer/{filename}")
