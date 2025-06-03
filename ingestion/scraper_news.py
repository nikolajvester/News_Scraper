from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_ai_news():
    url = "https://www.technologyreview.com/topic/artificial-intelligence/"  # Example AI news site

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Wait for articles to load (adjust selector for your target site)
        page.wait_for_selector("article")

        # Get full HTML content
        html = page.content()
        browser.close()

    # Use BeautifulSoup to extract article titles
    soup = BeautifulSoup(html, "lxml")
    articles = soup.find_all("article")

    for idx, article in enumerate(articles[:5], start=1):  # Limit to 5 for now
        headline = article.get_text(strip=True)
        print(f"{idx}. {headline[:120]}...")  # Preview first 120 chars

if __name__ == "__main__":
    scrape_ai_news()
