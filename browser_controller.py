from playwright.async_api import async_playwright
import asyncio

class BrowserController:
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
        
    async def init_browser(self, proxy=None):
        self.playwright = await async_playwright().start()
        browser_args = {}
        
        if proxy:
            browser_args['proxy'] = {
                'server': proxy
            }
            
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            proxy=browser_args.get('proxy')
        )
        
        self.page = await self.browser.new_page()
        
    async def visit_url(self, url):
        try:
            await self.page.goto(url)
            return await self.page.content()
        except Exception as e:
            return f"访问出错: {str(e)}"
            
    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop() 