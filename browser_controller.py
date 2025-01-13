from playwright.async_api import async_playwright
import asyncio

class BrowserController:
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
        
    async def init_browser(self, proxy=None):
        """初始化浏览器"""
        try:
            self.playwright = await async_playwright().start()
            if proxy:
                browser_args = {
                    'proxy': {
                        'server': f"socks5://{proxy.split('://')[1]}",
                    }
                }
                self.browser = await self.playwright.chromium.launch(proxy=browser_args['proxy'])
                
                # 获取当前代理IP
                page = await self.browser.new_page()
                await page.goto('http://httpbin.org/ip')
                content = await page.content()
                await page.close()
                
                # 解析IP信息
                import json
                import re
                ip_match = re.search(r'"origin":\s*"([^"]+)"', content)
                if ip_match:
                    self.current_ip = ip_match.group(1)
                else:
                    self.current_ip = "未知"
                
            else:
                self.browser = await self.playwright.chromium.launch()
                self.current_ip = "未使用代理"
            
            self.page = await self.browser.new_page()
            return True
        except Exception as e:
            return f"浏览器初始化失败: {str(e)}"
            
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

    def get_current_ip(self):
        """获取当前使用的IP"""
        return getattr(self, 'current_ip', "未知") 