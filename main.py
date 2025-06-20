from ingestion.scraper_news import scrape_site
from storage.db import init_db

# Configs
from configs.theverge import config as theverge_config
from configs.techcrunch import config as techcrunch_config

def main():
    init_db()               # ensure DB exists
    scrape_site(theverge_config)

if __name__ == "__main__":
    main()