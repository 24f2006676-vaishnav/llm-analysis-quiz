from playwright.async_api import async_playwright

async def load_quiz_page(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        
        # Wait for dynamic content to load
        await page.wait_for_timeout(1000)

        # Extract the entire rendered HTML
        content = await page.content()

        await browser.close()
        return content
