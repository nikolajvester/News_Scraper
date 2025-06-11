from playwright.sync_api import sync_playwright
from storage.db import url_exists
from bs4 import BeautifulSoup
from processing.summarize import summarize_text
from storage.db import insert_summary
import time

if url_exists(url):
    print(f"⚠️ Skipping previously summarized article: {url}")
    continue


def scrape_article_text(page, url):
    page.goto(url, timeout=60000)
    page.wait_for_selector("p.duet--article--dangerously-set-cms-markup.duet--article--standard-paragraph", timeout=15000)
    html = page.content()
    soup = BeautifulSoup(html, "lxml")
    paragraphs = soup.select("p.duet--article--dangerously-set-cms-markup.duet--article--standard-paragraph")
    full_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
    return full_text

def scrape_theverge_ai():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.theverge.com/ai-artificial-intelligence", timeout=60000)
        page.wait_for_selector("div.duet--content-cards--content-card")
        html = page.content()

        soup = BeautifulSoup(html, "lxml")
        articles = soup.select("div.duet--content-cards--content-card")

        print(f"📰 Found {len(articles)} articles\n")

        for article in articles:
            a_tag = article.select_one("a")
            if not a_tag:
                continue

            title = a_tag.get("aria-label", "").strip()
            relative_link = a_tag.get("href", "").strip()
            url = "https://www.theverge.com" + relative_link

            try:
                print(f"🔗 Visiting: {title}")
                full_article = scrape_article_text(page, url)
                summary = summarize_text(full_article)
                insert_summary(title, url, summary)
                print("✅ Summary saved\n")
                time.sleep(2)
            except Exception as e:
                print(f"❌ Failed on {url}: {e}")
                continue

        browser.close()
