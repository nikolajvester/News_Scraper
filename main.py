from ingestion.scraper_news import scrape_theverge_ai
from storage.db import init_db

def main():
    init_db()               # ensure DB exists
    scrape_theverge_ai()    # scrape, summarize, and store

if __name__ == "__main__":
    main()
