# Transfermarkt Scrapper API

## Requirements
- Python 3.9 (or around the version)
- Poetry Package Manager
- Splash (running at [http://localhost:8050](http://localhost:8050))

## Setup The Project

1. clone the project and go the directory by console.
1. run `poetry install`
1. create empty `databases/transfermarkt.db` file
1. run `poetry run alembic upgrade head`
1. duplicate `transfermarkt_scrapper/settings.py.backup` into `transfermarkt_scrapper/settings.py` and set the preferences in the file
1. run `poetry run scrapy crawl transfers` to start the crawl


