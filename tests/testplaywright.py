from playwright.sync_api import sync_playwright

def test_playwright():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto("https://example.com", timeout=60000)
        print("✅ Page loaded.")
        print("Title:", page.title())
        page.screenshot(path="test_screenshot.png")

        input("🔍 Press Enter to close the browser...")
        browser.close()

test_playwright()

