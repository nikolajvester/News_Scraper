# News Scraper
## 🚀 Overview
### This repository hosts a robust Python-based news scraper designed to automatically extract and centralize articles from various news sources. Built with Playwright for handling dynamic web content, it ensures reliable data collection even from modern, JavaScript-heavy websites. All scraped information is directly stored in a SQLite database, making it easy to analyze or integrate with other applications.

Currently, the scraper is configured to collect news from TechCrunch and The Verge.

#### ✨ Features
Dynamic Content Scraping: Utilizes Playwright to effectively navigate and scrape content from websites that rely heavily on JavaScript.
Structured Data Extraction: Captures key information for each article, including:
- Title
- URL
- Publication Date
- Full Article Text
- Summary
- Primary Category
- Secondary Category
- Direct SQLite Database Storage: Seamlessly inserts all extracted data directly into a local SQLite database for organized and accessible storage.
- Configurable Sources: Easily extensible to add new news sources by defining them as configuration files.

#### Technologies Used
- Python 3.12
- Playwright: For browser automation and dynamic content scraping.
- sqlite3 (Python's built-in module): For interacting with the SQLite database.
- BeautifulSoup4: For HTML parsing.
- SQLite: The chosen database for data storage.
- Transformers: For zero-shot classification

#### Usage
The scraper is initiated via main.py. It reads the configured news sources and processes them.

Configure News Sources:

The scraper currently supports TechCrunch and The Verge.
News sources are defined as configuration files. You will need to edit these files to add or modify sources.
Run the Scraper:
Navigate to the directory containing main.py and execute:

#### Contact
For any questions or inquiries, feel free to reach out:

Email: nikolaj.vester@gmail.com
LinkedIn: Nikolaj Vestergaard
