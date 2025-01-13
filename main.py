import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
from main_window import MainWindow
from browser_controller import BrowserController
import asyncio
from queue import Queue, Empty
import random

class ProxyBrowser:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.browser_threads = []
        self.url_queue = Queue()
        
        # 连接信号
        self.window.start_btn.clicked.connect(self.start_browsing)
        self.window.stop_btn.clicked.connect(self.stop_browsing)
        
    def start_browsing(self):
        # 清空之前的队列
        while not self.url_queue.empty():
            self.url_queue.get()
            
        # 获取URLs
        urls = self.window.url_input.toPlainText().strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        
        if not urls:
            self.window.log_text.append("请输入要访问的URL")
            return
            
        # 获取当前代理
        proxy = self.window.get_current_proxy()
        if not proxy:
            self.window.log_text.append("请先设置并测试代理")
            return
            
        # 获取时间范围设置
        time_range = self.window.get_time_range()
        
        # 获取浏览器模式
        headless = self.window.get_browser_mode()
        
        # 将URLs添加到队列
        for url in urls:
            self.url_queue.put(url)
            
        thread_count = min(self.window.thread_slider.value(), len(urls))
        
        # 创建并启动线程
        for _ in range(thread_count):
            thread = BrowserThread(
                self.url_queue, 
                proxy, 
                time_range,
                headless
            )
            thread.log_signal.connect(self.window.log_text.append)
            thread.start()
            self.browser_threads.append(thread)
            
    def stop_browsing(self):
        for thread in self.browser_threads:
            if thread.isRunning():
                thread.stop()
                thread.wait()
        
        self.browser_threads.clear()
        self.window.log_text.append("已停止所有浏览任务")
        
    def run(self):
        self.window.show()
        return self.app.exec()

class BrowserThread(QThread):
    log_signal = pyqtSignal(str)
    
    def __init__(self, url_queue, proxy, time_range, headless):
        super().__init__()
        self.url_queue = url_queue
        self.proxy = proxy
        self.time_range = time_range
        self.headless = headless
        self.browser_controller = BrowserController()
        self.is_running = True
        
    def run(self):
        async def async_browse():
            try:
                await self.browser_controller.init_browser(
                    self.proxy, 
                    headless=self.headless
                )
                current_ip = self.browser_controller.get_current_ip()
                self.log_signal.emit(f"浏览器已初始化，使用IP: {current_ip}")
                
                while self.is_running:
                    try:
                        url = self.url_queue.get_nowait()
                        self.log_signal.emit(f"正在访问: {url} (使用IP: {current_ip})")
                        content = await self.browser_controller.visit_url(url)
                        
                        # 随机等待时间
                        wait_time = random.randint(
                            self.time_range['min_time'],
                            self.time_range['max_time']
                        )
                        self.log_signal.emit(f"停留 {wait_time} 秒...")
                        await asyncio.sleep(wait_time)
                        
                        self.log_signal.emit(f"访问成功: {url}")
                    except Empty:
                        break
            except Exception as e:
                self.log_signal.emit(f"错误: {str(e)}")
            finally:
                await self.browser_controller.close()
        
        asyncio.run(async_browse())
        
    def stop(self):
        self.is_running = False

if __name__ == "__main__":
    browser = ProxyBrowser()
    sys.exit(browser.run()) 