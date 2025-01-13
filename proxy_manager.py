import json
import os
import asyncio
import aiohttp
import random
from PyQt6.QtCore import QThread, QTimer

class AsyncioThread(QThread):
    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

class ProxyManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.proxy_input = None
        self.proxy_status = None
        
        # 创建并启动异步事件循环线程
        self.asyncio_thread = AsyncioThread()
        self.asyncio_thread.start()
        
        # 等待事件循环准备好
        while not hasattr(self.asyncio_thread, 'loop'):
            pass
        
        self.loop = self.asyncio_thread.loop
        
        # 添加防抖定时器
        self.save_timer = None
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self._do_save_config)
        
    def generate_proxy_session(self):
        """生成新的代理会话信息"""
        try:
            proxy_text = self.proxy_input.text().strip()
            if not proxy_text:
                raise ValueError("请输入代理信息")
                
            parts = proxy_text.split(':')
            if len(parts) != 4:
                raise ValueError("代理格式错误，应为: 服务器:端口:用户名格式:密码")
                
            host, port, username_format, password = parts
            session_id = str(random.randint(100000000, 999999999))
            username = username_format.replace("{sid}", session_id)
            
            proxy_info = {
                'host': host,
                'port': port,
                'username': username,
                'password': password,
                'full_proxy': f"http://{username}:{password}@{host}:{port}"
            }
            
            self.current_proxy = proxy_info
            self.proxy_status.setText(f"当前代理: {host}:{port} (会话ID: {session_id})")
            return proxy_info
            
        except Exception as e:
            self.main_window.log_text.append(f"生成代理会话失败: {str(e)}")
            return None
            
    def get_current_proxy(self):
        """获取新的代理信息（每次调用都生成新会话）"""
        proxy_info = self.generate_proxy_session()
        if proxy_info:
            # 确保返回完整的代理信息字典
            return {
                'host': proxy_info['host'],
                'port': proxy_info['port'],
                'username': proxy_info['username'],
                'password': proxy_info['password'],
                'full_proxy': proxy_info['full_proxy']
            }
        return None
        
    async def test_proxy(self):
        """测试当前代理"""
        proxy_info = self.generate_proxy_session()
        if not proxy_info:
            return
            
        try:
            from aiohttp_socks import ProxyConnector
            connector = ProxyConnector.from_url(proxy_info['full_proxy'])
            
            async with aiohttp.ClientSession(connector=connector) as session:
                self.main_window.log_text.append(f"正在测试代理: {proxy_info['host']}:{proxy_info['port']}")
                async with session.get('http://httpbin.org/ip') as response:
                    if response.status == 200:
                        result = await response.json()
                        self.main_window.log_text.append(f"代理测试成功: {result.get('origin')}")
                    else:
                        self.main_window.log_text.append(f"代理测试失败: HTTP {response.status}")
        except Exception as e:
            self.main_window.log_text.append(f"代理测试出错: {str(e)}")
            
    def handle_test_proxy(self):
        """处理测试代理按钮点击"""
        future = asyncio.run_coroutine_threadsafe(self.test_proxy(), self.loop)
        future.add_done_callback(lambda f: self.handle_async_result(f, "测试代理"))
        
    def handle_async_result(self, future, operation):
        """处理异步操作的结果"""
        try:
            future.result()
        except Exception as e:
            self.main_window.log_text.append(f"{operation}时发生错误: {str(e)}")
            
    def save_config(self, show_message=True):
        """保存配置到文件（带防抖）"""
        if self.save_timer:
            self.save_timer.stop()
        self.save_timer.start(1000)  # 1秒后执行保存
        self.show_save_message = show_message
        
    def _do_save_config(self):
        """实际执行配置保存"""
        config = {
            'urls': self.main_window.url_input.toPlainText(),
            'proxy_string': self.proxy_input.text(),
            'thread_count': self.main_window.thread_slider.value(),
            'min_time': self.main_window.min_time_input.value(),
            'max_time': self.main_window.max_time_input.value(),
            'min_interval': self.main_window.min_interval_input.value(),
            'max_interval': self.main_window.max_interval_input.value(),
            'headless': self.main_window.get_browser_mode()
        }
        
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            if getattr(self, 'show_save_message', True):
                self.main_window.log_text.append("配置已保存")
        except Exception as e:
            self.main_window.log_text.append(f"保存配置失败: {str(e)}")
            
    def load_config(self):
        """从文件加载配置"""
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # 暂时禁用自动保存
                self.main_window.url_input.blockSignals(True)
                self.proxy_input.blockSignals(True)
                self.main_window.thread_slider.blockSignals(True)
                self.main_window.min_time_input.blockSignals(True)
                self.main_window.max_time_input.blockSignals(True)
                self.main_window.min_interval_input.blockSignals(True)
                self.main_window.max_interval_input.blockSignals(True)
                
                try:
                    # 加载配置
                    self.main_window.url_input.setPlainText(config.get('urls', ''))
                    self.proxy_input.setText(config.get('proxy_string', ''))
                    self.main_window.thread_slider.setValue(config.get('thread_count', 3))
                    self.main_window.min_time_input.setValue(config.get('min_time', 10))
                    self.main_window.max_time_input.setValue(config.get('max_time', 20))
                    self.main_window.min_interval_input.setValue(config.get('min_interval', 5))
                    self.main_window.max_interval_input.setValue(config.get('max_interval', 15))
                    
                    # 设置浏览器模式
                    headless = config.get('headless', False)
                    for button in self.main_window.browser_mode_group.buttons():
                        if (button.text() == "无头模式（后台运行）") == headless:
                            button.setChecked(True)
                            break
                        
                    if config.get('proxy_string'):
                        self.generate_proxy_session()
                        
                    self.main_window.log_text.append("配置已加载")
                finally:
                    # 恢复自动保存
                    self.main_window.url_input.blockSignals(False)
                    self.proxy_input.blockSignals(False)
                    self.main_window.thread_slider.blockSignals(False)
                    self.main_window.min_time_input.blockSignals(False)
                    self.main_window.max_time_input.blockSignals(False)
                    self.main_window.min_interval_input.blockSignals(False)
                    self.main_window.max_interval_input.blockSignals(False)
            else:
                self.main_window.log_text.append("未找到配置文件")
        except Exception as e:
            self.main_window.log_text.append(f"加载配置失败: {str(e)}")
            
    def close(self):
        """关闭代理管理器"""
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.asyncio_thread.wait() 