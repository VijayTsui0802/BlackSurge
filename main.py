import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QThread, pyqtSignal
from main_window import MainWindow
from browser_controller import BrowserController
import asyncio
from queue import Queue, Empty
import random
import threading

class ProxyBrowser:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.browser_threads = []
        self.url_list = []
        self.url_lock = threading.Lock()
        self.stopping = False
        self.stop_thread = None  # 添加停止线程的引用
        
        # 连接信号
        self.window.start_btn.clicked.connect(self.start_browsing)
        self.window.stop_btn.clicked.connect(self.stop_browsing)
        
    def start_browsing(self):
        # 如果正在停止，等待停止完成
        if self.stopping:
            self.window.log_text.append("正在等待之前的任务停止...")
            return
            
        # 清空之前的URL列表
        self.url_list.clear()
        
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
                        self.url_list.append(url.strip())
                        total_tasks += 1
                except ValueError:
                    self.window.log_text.append(f"错误的访问次数格式: {url_line}")
            else:
                self.url_list.append(url_line.strip())
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
        
        # 停止现有线程（如果有）
        if self.browser_threads:
            self.stop_browsing()
            # 等待停止完成
            while self.stopping:
                QThread.msleep(100)
        
        # 创建并启动线程
        for i in range(thread_count):
            thread = BrowserThread(
                self.url_list,
                self.window.proxy_manager,
                time_range,
                headless,
                f"线程-{i+1}",
                self.url_lock
            )
            thread.log_signal.connect(self.window.log_text.append)
            thread.start()
            self.browser_threads.append(thread)
            
        self.window.log_text.append(f"已启动 {thread_count} 个线程，总任务数: {total_tasks}")

    def stop_browsing(self):
        """停止所有浏览线程"""
        if self.stopping:
            self.window.log_text.append("正在等待停止完成...")
            return
            
        if not self.browser_threads:
            self.window.log_text.append("没有正在运行的任务")
            return
            
        self.stopping = True
        self.window.log_text.append("正在停止所有浏览任务...")
        self.window.stop_btn.setEnabled(False)
        
        # 创建停止线程
        class StopThread(QThread):
            def __init__(self, browser):
                super().__init__()
                self.browser = browser
                
            def run(self):
                self.browser._stop_threads()
        
        self.stop_thread = StopThread(self)
        self.stop_thread.finished.connect(self._on_stop_complete)
        self.stop_thread.start()
    
    def _stop_threads(self):
        """在单独的线程中停止所有浏览线程"""
        try:
            # 停止所有线程
            for thread in self.browser_threads[:]:  # 使用列表副本进行迭代
                if thread and thread.isRunning():
                    thread.stop()
                    # 等待线程结束，最多等待5秒
                    for _ in range(50):  # 50 * 100ms = 5秒
                        if not thread.isRunning():
                            break
                        QThread.msleep(100)
                    
            # 清空线程列表
            self.browser_threads.clear()
            
            # 清空URL列表
            with self.url_lock:
                self.url_list.clear()
                
        except Exception as e:
            self.window.log_text.append(f"停止过程出错: {str(e)}")
    
    def _on_stop_complete(self):
        """停止完成后的回调"""
        self.stopping = False
        self.window.stop_btn.setEnabled(True)
        self.window.log_text.append("已停止所有浏览任务")
        # 清理停止线程
        if self.stop_thread:
            self.stop_thread.deleteLater()
            self.stop_thread = None

    def run(self):
        """启动应用程序"""
        self.window.show()
        return self.app.exec()

class BrowserThread(QThread):
    log_signal = pyqtSignal(str)
    
    def __init__(self, url_list, proxy_manager, time_range, headless, thread_name, url_lock):
        super().__init__()
        self.url_list = url_list
        self.url_lock = url_lock
        self.proxy_manager = proxy_manager
        self.time_range = time_range
        self.headless = headless
        self.thread_name = thread_name
        self.is_running = True
        self.browser_controller = None
        self.loop = None
        
    def run(self):
        # 创建新的事件循环
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        try:
            while self.is_running:
                try:
                    url = None
                    # 使用线程锁保护URL列表的访问
                    with self.url_lock:
                        if not self.url_list:  # 检查URL列表是否为空
                            break
                        # 随机选择一个URL
                        url = random.choice(self.url_list)
                        # 从列表中移除已选择的URL
                        self.url_list.remove(url)
                    
                    if not url or not self.is_running:  # 再次检查运行状态
                        break
                        
                    try:
                        # 创建新的浏览器实例
                        self.browser_controller = BrowserController()
                        # 在事件循环中执行浏览任务
                        self.loop.run_until_complete(self.browse_url(url))
                        
                        if not self.is_running:  # 检查是否需要停止
                            break
                            
                    except Exception as e:
                        self.log_signal.emit(f"{self.thread_name} 访问出错: {str(e)}")
                    finally:
                        # 确保浏览器被关闭
                        if self.browser_controller:
                            try:
                                self.loop.run_until_complete(self.browser_controller.close())
                                self.browser_controller = None
                            except Exception as e:
                                self.log_signal.emit(f"{self.thread_name} 关闭浏览器出错: {str(e)}")
                        
                except Exception as e:
                    self.log_signal.emit(f"{self.thread_name} 错误: {str(e)}")
                    if not self.is_running:  # 检查是否需要停止
                        break
                        
                # 检查是否需要停止
                if not self.is_running:
                    break
        finally:
            # 确保退出前清理所有资源
            self._cleanup_resources()
            self.log_signal.emit(f"{self.thread_name} 已完成所有任务")
    
    def _cleanup_resources(self):
        """清理所有资源"""
        try:
            # 关闭浏览器
            if self.browser_controller and self.loop and not self.loop.is_closed():
                try:
                    self.loop.run_until_complete(self.browser_controller.close())
                except:
                    pass
                self.browser_controller = None
            
            # 清理事件循环
            if self.loop and not self.loop.is_closed():
                try:
                    # 取消所有待处理的任务
                    pending = asyncio.all_tasks(self.loop)
                    if pending:
                        self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
                    # 关闭事件循环
                    self.loop.run_until_complete(self.loop.shutdown_asyncgens())
                    self.loop.close()
                except:
                    pass
                self.loop = None
        except:
            pass
    
    def stop(self):
        """停止线程"""
        self.is_running = False
        self._cleanup_resources()
    
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

if __name__ == "__main__":
    browser = ProxyBrowser()
    sys.exit(browser.run()) 