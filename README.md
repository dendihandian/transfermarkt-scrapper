# Transfermarkt Scrapper API

## Requirements
- Python 3.9 (or around the version)
- Poetry Package Manager
- Splash (running at [http://localhost:8050](http://localhost:8050))

## The Development Setup

1. clone the project and go the directory by console.
1. run `poetry install`
1. create empty `data/transfermarkt.db` file
1. run `poetry run alembic upgrade head`
1. duplicate `transfermarkt_scrapper/settings.py.backup` into `transfermarkt_scrapper/settings.py` and set the preferences in the file
1. run `poetry run scrapy crawl transfers` to start the crawl

## Appendix

### migrate to an empty or outdated database

```
poetry run alembic upgrade head
```

### create a migration/revision script

```
poetry run alembic revision -m "create account table"
```

### create a spider

```
poetry run scrapy genspider your-spider-name the-url.com
```

### monitoring transfer counts query
```sql
SELECT
	transfer_date_p,
	COUNT(1) as count
FROM transfers
GROUP BY transfer_date_p
ORDER BY transfer_date_p DESC
```