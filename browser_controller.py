from playwright.async_api import async_playwright
import asyncio
import re

class BrowserController:
    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
        self.current_ip = "未知"
        
    async def init_browser(self, proxy=None, headless=False):
        """初始化浏览器"""
        try:
            print(f"正在启动浏览器，模式: {'无头' if headless else '可见'}")
            self.playwright = await async_playwright().start()
            
            # 基本浏览器选项
            browser_options = {
                'headless': headless,  # 是否无头模式
                'args': [
                    '--start-maximized',
                    '--disable-infobars',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--window-position=0,0',
                ],
            }
            
            if proxy:
                # 从代理信息中提取服务器地址和认证信息
                browser_options['proxy'] = {
                    'server': f"http://{proxy['host']}:{proxy['port']}",  # 改为 http
                    'username': proxy['username'],
                    'password': proxy['password']
                }
                print(f"使用代理: {proxy['host']}:{proxy['port']}")
            
            # 启动浏览器
            self.browser = await self.playwright.chromium.launch(**browser_options)
            print("浏览器已启动")
            
            # 创建上下文，设置窗口大小
            context = await self.browser.new_context(
                no_viewport=True,  # 禁用视窗限制
                ignore_https_errors=True,
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            )
            
            # 创建新页面用于实际访问
            self.page = await context.new_page()
            
            # 最大化窗口
            await self.page.evaluate("""
                window.moveTo(0, 0);
                window.resizeTo(screen.width, screen.height);
            """)
            
            # 设置页面事件监听
            self.page.on("load", lambda _: print("页面加载完成"))
            self.page.on("dialog", lambda dialog: dialog.accept())
            
            # 获取当前代理IP（可选）
            if proxy:
                try:
                    # 正确使用 async with
                    test_page = await context.new_page()
                    try:
                        await test_page.goto('http://httpbin.org/ip', wait_until='load', timeout=10000)
                        content = await test_page.content()
                        ip_match = re.search(r'"origin":\s*"([^"]+)"', content)
                        self.current_ip = ip_match.group(1) if ip_match else "未知"
                    finally:
                        await test_page.close()
                except Exception as e:
                    print(f"获取IP失败: {str(e)}")
                    self.current_ip = f"{proxy['host']}:{proxy['port']}"
            else:
                self.current_ip = "未使用代理"
            
            return True
            
        except Exception as e:
            self.current_ip = "未知"
            print(f"浏览器初始化失败: {str(e)}")  # 添加错误输出
            return f"浏览器初始化失败: {str(e)}"
            
    async def visit_url(self, url):
        """访问指定URL"""
        try:
            print(f"正在访问: {url}")
            # 设置页面超时
            self.page.set_default_timeout(60000)  # 增加到60秒超时
            
            # 访问页面，使用 load 事件而不是 networkidle
            response = await self.page.goto(
                url, 
                wait_until='load',  # 改为 load
                timeout=60000  # 单独设置导航超时
            )
            
            if not response.ok:
                return f"访问失败: HTTP {response.status}"
            
            # 等待页面加载完成，使用较短的超时
            try:
                await self.page.wait_for_load_state('networkidle', timeout=10000)
            except:
                print("等待网络空闲超时，继续执行")
            
            # 执行滚动操作模拟真实浏览
            await self.page.evaluate("""
                window.scrollTo({
                    top: document.body.scrollHeight,
                    behavior: 'smooth'
                });
            """)
            
            await asyncio.sleep(2)  # 等待滚动完成
            
            # 滚动回顶部
            await self.page.evaluate("""
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            """)
            
            return await self.page.content()
            
        except Exception as e:
            print(f"访问出错: {str(e)}")  # 添加错误输出
            return f"访问出错: {str(e)}"
            
    async def close(self):
        """关闭浏览器"""
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
            
    def get_current_ip(self):
        """获取当前使用的IP"""
        return self.current_ip 