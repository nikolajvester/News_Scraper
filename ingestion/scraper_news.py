# Project Def.
from playwright.sync_api import sync_playwright
from processing.categorize import categorize_text
from processing.categorize import categorize_text
from storage.db import url_exists
from processing.summarize import summarize_text
from storage.db import insert_summary

# Library imports
from bs4 import BeautifulSoup
import time

def scrape_article_text(page, url):
    page.goto(url, timeout=60000)
    page.wait_for_selector("p.duet--article--dangerously-set-cms-markup.duet--article--standard-paragraph", timeout=15000)
    html = page.content()
    soup = BeautifulSoup(html, "lxml")
    paragraphs = soup.select("p.duet--article--dangerously-set-cms-markup.duet--article--standard-paragraph")
    full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
    return full_text

def scrape_site(config):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(config["listing_url"], timeout=60000)
        page.wait_for_selector(config["article_selector"])
        soup = BeautifulSoup(page.content(), "lxml")
        articles = soup.select(config["article_selector"])

        print(f"📰 [{config['site_name']}] Found {len(articles)} articles\n")

        for article in articles:
            a_tag = article.select_one("a")
            if not a_tag:
                continue

            title = a_tag.get(config["title_attr"], "").strip() or a_tag.get_text(strip=True)
            if not title:
                headline = article.find("h2") or article.find("h3") or article.find("h1")
                title = headline.get_text(strip=True) if headline else ""

            relative_link = a_tag.get(config["link_attr"], "").strip()
            url = config["base_url"] + relative_link

            if url_exists(url):
                print(f"⚠️ Skipping previously summarized article: {url}")
                continue

            try:
                print(f"🔗 Visiting: {title}")
                page.goto(url, timeout=60000)
                page.wait_for_selector(config["paragraph_selector"], timeout=15000)
                article_soup = BeautifulSoup(page.content(), "lxml")
                paragraphs = article_soup.select(config["paragraph_selector"])
                full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

                summary = summarize_text(full_text)
                primary, secondary = categorize_text(summary)

                insert_summary(
                    title, url, summary,
                    primary_category=primary,
                    secondary_categories=secondary,
                    source=config["site_name"]
                )
                print("✅ Summary saved\n")
                time.sleep(2)

            except Exception as e:
                print(f"❌ Failed on {url}: {e}")
                continue

        browser.close()