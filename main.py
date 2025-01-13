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
        # 清空之前的队列和线程
        while not self.url_queue.empty():
            self.url_queue.get()
        self.stop_browsing()
        
        # 获取URLs和访问次数
        urls = self.window.url_input.toPlainText().strip().split('\n')
        total_tasks = 0
        
        for url_line in urls:
            if not url_line.strip():
                continue
                
            if '----' in url_line:
                url, count = url_line.split('----')
                try:
                    count = int(count)
                    for _ in range(count):
                        self.url_queue.put(url.strip())
                        total_tasks += 1
                except ValueError:
                    self.window.log_text.append(f"错误的访问次数格式: {url_line}")
            else:
                self.url_queue.put(url_line.strip())
                total_tasks += 1
        
        if total_tasks == 0:
            self.window.log_text.append("请输入要访问的URL")
            return
            
        # 获取代理管理器而不是具体的代理
        if not self.window.proxy_manager.proxy_input.text().strip():
            self.window.log_text.append("请先设置代理")
            return
            
        # 获取时间范围设置
        time_range = self.window.get_time_range()
        
        # 获取浏览器模式
        headless = self.window.get_browser_mode()
        
        # 获取线程数
        thread_count = self.window.thread_slider.value()
        
        # 创建并启动线程
        for i in range(thread_count):
            thread = BrowserThread(
                self.url_queue, 
                self.window.proxy_manager,  # 传入代理管理器
                time_range,
                headless,
                f"线程-{i+1}"
            )
            thread.log_signal.connect(self.window.log_text.append)
            thread.start()
            self.browser_threads.append(thread)
            
        self.window.log_text.append(f"已启动 {thread_count} 个线程，总任务数: {total_tasks}")

    def stop_browsing(self):
        """停止所有浏览线程"""
        # 停止所有线程
        for thread in self.browser_threads:
            if thread.isRunning():
                thread.stop()
                thread.wait()  # 等待线程结束
        
        # 清空线程列表
        self.browser_threads.clear()
        
        # 清空队列
        while not self.url_queue.empty():
            self.url_queue.get()
            
        self.window.log_text.append("已停止所有浏览任务")
        
    def run(self):
        """启动应用程序"""
        self.window.show()
        return self.app.exec()

class BrowserThread(QThread):
    log_signal = pyqtSignal(str)
    
    def __init__(self, url_queue, proxy_manager, time_range, headless, thread_name):
        super().__init__()
        self.url_queue = url_queue
        self.proxy_manager = proxy_manager
        self.time_range = time_range
        self.headless = headless
        self.thread_name = thread_name
        self.is_running = True
        self.browser_controller = None
        
    def run(self):
        while self.is_running:
            try:
                # 获取下一个URL，如果队列为空则退出
                try:
                    url = self.url_queue.get_nowait()
                except Empty:
                    break
                
                try:
                    # 创建新的浏览器实例
                    self.browser_controller = BrowserController()
                    # 异步执行浏览任务
                    asyncio.run(self.browse_url(url))
                except Exception as e:
                    self.log_signal.emit(f"{self.thread_name} 访问出错: {str(e)}")
                finally:
                    # 确保浏览器被关闭
                    if self.browser_controller:
                        try:
                            asyncio.run(self.browser_controller.close())
                            self.browser_controller = None
                        except Exception as e:
                            self.log_signal.emit(f"{self.thread_name} 关闭浏览器出错: {str(e)}")
                    
            except Exception as e:
                self.log_signal.emit(f"{self.thread_name} 错误: {str(e)}")
                
        self.log_signal.emit(f"{self.thread_name} 已完成所有任务")
    
    async def browse_url(self, url):
        """处理单个URL的访问"""
        try:
            # 每次访问获取新的代理会话
            proxy = self.proxy_manager.get_current_proxy()
            if not proxy:
                self.log_signal.emit(f"{self.thread_name} 获取代理失败")
                return
                
            # 初始化浏览器
            result = await self.browser_controller.init_browser(proxy, self.headless)
            if isinstance(result, str) and "失败" in result:
                self.log_signal.emit(f"{self.thread_name} {result}")
                return
                
            current_ip = self.browser_controller.get_current_ip()
            self.log_signal.emit(f"{self.thread_name} 使用IP: {current_ip}")
            
            # 访问网页
            self.log_signal.emit(f"{self.thread_name} 正在访问: {url}")
            await self.browser_controller.visit_url(url)
            
            # 随机停留时间
            stay_time = random.randint(
                self.time_range['min_time'],
                self.time_range['max_time']
            )
            self.log_signal.emit(f"{self.thread_name} 停留 {stay_time} 秒...")
            await asyncio.sleep(stay_time)
            
            # 关闭当前页面
            await self.browser_controller.page.close()
            await self.browser_controller.browser.close()
            
            # 随机间隔时间
            interval_time = random.randint(
                self.time_range['min_interval'],
                self.time_range['max_interval']
            )
            self.log_signal.emit(f"{self.thread_name} 等待间隔 {interval_time} 秒...")
            await asyncio.sleep(interval_time)
            
        except Exception as e:
            self.log_signal.emit(f"{self.thread_name} 浏览过程出错: {str(e)}")
            # 确保出错时也关闭浏览器
            if self.browser_controller:
                try:
                    await self.browser_controller.page.close()
                    await self.browser_controller.browser.close()
                except:
                    pass
    
    def stop(self):
        self.is_running = False
        # 确保停止时关闭浏览器
        if self.browser_controller:
            try:
                asyncio.run(self.browser_controller.close())
                self.browser_controller = None
            except:
                pass

if __name__ == "__main__":
    browser = ProxyBrowser()
    sys.exit(browser.run()) 