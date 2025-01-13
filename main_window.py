from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QTextEdit, QLineEdit, QLabel, QSpinBox,
                            QFrame, QSlider)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
import json
import os
import asyncio
import aiohttp

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("代理IP网站访问器")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(self.get_style_sheet())
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建顶部标题
        title_label = QLabel("代理IP网站访问工具")
        title_label.setObjectName("titleLabel")
        main_layout.addWidget(title_label)
        
        # 创建分隔线
        main_layout.addWidget(self.create_separator())
        
        # URL输入区域
        url_frame = QFrame()
        url_frame.setObjectName("inputFrame")
        url_layout = QVBoxLayout(url_frame)
        
        url_header = QLabel("URLs (每行一个):")
        url_header.setObjectName("sectionHeader")
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText("请输入要访问的网址，每行一个")
        self.url_input.setMinimumHeight(150)
        
        url_layout.addWidget(url_header)
        url_layout.addWidget(self.url_input)
        main_layout.addWidget(url_frame)
        
        # 代理设置区域
        proxy_frame = QFrame()
        proxy_frame.setObjectName("inputFrame")
        proxy_layout = QVBoxLayout(proxy_frame)
        
        proxy_header = QLabel("代理设置")
        proxy_header.setObjectName("sectionHeader")
        
        # 代理API设置
        api_layout = QVBoxLayout()
        api_label = QLabel("代理API链接:")
        api_label.setObjectName("controlLabel")
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("输入获取代理IP的API链接")
        
        # 代理信息显示区域
        proxy_info_layout = QVBoxLayout()
        proxy_info_layout.setSpacing(5)
        
        # 当前代理状态
        self.proxy_status = QLabel("当前未设置代理")
        self.proxy_status.setObjectName("proxyStatus")
        
        # 测试按钮
        test_btn_layout = QHBoxLayout()
        self.test_proxy_btn = QPushButton("测试代理")
        self.test_proxy_btn.setObjectName("secondaryButton")
        self.refresh_proxy_btn = QPushButton("刷新代理")
        self.refresh_proxy_btn.setObjectName("secondaryButton")
        
        test_btn_layout.addWidget(self.test_proxy_btn)
        test_btn_layout.addWidget(self.refresh_proxy_btn)
        test_btn_layout.addStretch()
        
        # 组装代理设置布局
        proxy_layout.addWidget(proxy_header)
        proxy_layout.addWidget(api_label)
        proxy_layout.addWidget(self.api_input)
        proxy_layout.addWidget(self.proxy_status)
        proxy_layout.addLayout(test_btn_layout)
        
        main_layout.addWidget(proxy_frame)
        
        # 线程控制区域
        control_frame = QFrame()
        control_frame.setObjectName("inputFrame")
        control_layout = QVBoxLayout(control_frame)
        
        # 标题和说明
        control_header = QLabel("线程控制")
        control_header.setObjectName("sectionHeader")
        control_desc = QLabel("调整同时访问的网站数量 (建议: 3-5个)")
        control_desc.setObjectName("descLabel")
        
        # 线程控制子布局
        thread_layout = QVBoxLayout()
        thread_layout.setSpacing(15)
        
        # 创建水平布局用于放置滑块
        slider_layout = QHBoxLayout()
        
        # 最小值标签
        min_label = QLabel("较慢\n1")
        min_label.setObjectName("rangeLabel")
        min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 最大值标签
        max_label = QLabel("较快\n10")
        max_label.setObjectName("rangeLabel")
        max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 创建滑块
        self.thread_slider = QSlider(Qt.Orientation.Horizontal)
        self.thread_slider.setRange(1, 10)
        self.thread_slider.setValue(3)
        self.thread_slider.setObjectName("threadSlider")
        
        # 添加到布局
        slider_layout.addWidget(min_label)
        slider_layout.addWidget(self.thread_slider)
        slider_layout.addWidget(max_label)
        
        # 添加当前状态显示
        self.thread_status = QLabel()
        self.thread_status.setObjectName("statusLabel")
        self.update_thread_status(3)  # 初始状态
        
        # 组装布局
        thread_layout.addWidget(control_desc)
        thread_layout.addLayout(slider_layout)
        thread_layout.addWidget(self.thread_status)
        
        control_layout.addWidget(control_header)
        control_layout.addLayout(thread_layout)
        main_layout.addWidget(control_frame)
        
        # 连接信号
        self.thread_slider.valueChanged.connect(self.update_thread_status)
        
        # 按钮区域
        button_frame = QFrame()
        button_frame.setObjectName("buttonFrame")
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(10)
        
        self.start_btn = QPushButton("开始访问")
        self.stop_btn = QPushButton("停止")
        self.save_btn = QPushButton("保存配置")
        self.load_btn = QPushButton("加载配置")
        
        for btn in [self.start_btn, self.stop_btn, self.save_btn, self.load_btn]:
            btn.setMinimumWidth(120)
            btn.setMinimumHeight(35)
            button_layout.addWidget(btn)
        
        self.start_btn.setObjectName("primaryButton")
        self.stop_btn.setObjectName("dangerButton")
        
        main_layout.addWidget(button_frame)
        
        # 日志显示区域
        log_frame = QFrame()
        log_frame.setObjectName("logFrame")
        log_layout = QVBoxLayout(log_frame)
        
        log_header = QLabel("运行日志")
        log_header.setObjectName("sectionHeader")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        
        log_layout.addWidget(log_header)
        log_layout.addWidget(self.log_text)
        main_layout.addWidget(log_frame)
        
        # 连接信号
        self.save_btn.clicked.connect(self.save_config)
        self.load_btn.clicked.connect(self.load_config)
        
        # 创建事件循环
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # 修改按钮连接
        self.test_proxy_btn.clicked.connect(self.handle_test_proxy)
        self.refresh_proxy_btn.clicked.connect(self.handle_refresh_proxy)
        
    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator
        
    def get_style_sheet(self):
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            #titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px 0;
            }
            
            #sectionHeader {
                font-size: 16px;
                font-weight: bold;
                color: #34495e;
                padding: 5px 0;
            }
            
            #inputFrame, #logFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #dcdde1;
            }
            
            QTextEdit, QLineEdit {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                selection-background-color: #3498db;
            }
            
            QSpinBox {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
            
            QPushButton {
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
                border: none;
            }
            
            #primaryButton {
                background-color: #3498db;
                color: white;
            }
            
            #primaryButton:hover {
                background-color: #2980b9;
            }
            
            #dangerButton {
                background-color: #e74c3c;
                color: white;
            }
            
            #dangerButton:hover {
                background-color: #c0392b;
            }
            
            QPushButton:not(#primaryButton):not(#dangerButton) {
                background-color: #95a5a6;
                color: white;
            }
            
            QPushButton:not(#primaryButton):not(#dangerButton):hover {
                background-color: #7f8c8d;
            }
            
            #buttonFrame {
                padding: 10px;
            }
            
            #controlLabel {
                font-size: 14px;
                color: #34495e;
                min-width: 80px;
            }
            
            #threadSlider {
                height: 25px;
                margin: 0 10px;
            }
            
            #threadSlider::groove:horizontal {
                border: 1px solid #bdc3c7;
                height: 8px;
                background: #ecf0f1;
                margin: 2px 0;
                border-radius: 4px;
            }
            
            #threadSlider::handle:horizontal {
                background: #3498db;
                border: none;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            
            #threadSlider::handle:horizontal:hover {
                background: #2980b9;
            }
            
            #threadSpinBox {
                min-width: 60px;
                max-width: 60px;
                padding: 3px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background: white;
            }
            
            #valueLabel {
                color: #2980b9;
                font-size: 13px;
                margin-top: 5px;
            }
            
            #threadSlider::sub-page:horizontal {
                background: #3498db;
                border-radius: 4px;
            }
            
            #descLabel {
                color: #7f8c8d;
                font-size: 13px;
                margin-bottom: 10px;
            }
            
            #rangeLabel {
                color: #7f8c8d;
                font-size: 12px;
                min-width: 40px;
            }
            
            #statusLabel {
                color: #2980b9;
                font-size: 14px;
                padding: 10px;
                margin-top: 5px;
                background: #ecf0f1;
                border-radius: 4px;
                text-align: center;
            }
            
            #threadSlider {
                height: 30px;
                margin: 0 15px;
            }
            
            #threadSlider::groove:horizontal {
                border: 1px solid #bdc3c7;
                height: 10px;
                background: #ecf0f1;
                margin: 0;
                border-radius: 5px;
            }
            
            #threadSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: none;
                width: 22px;
                height: 22px;
                margin: -6px 0;
                border-radius: 11px;
            }
            
            #threadSlider::handle:horizontal:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2980b9, stop:1 #2475a8);
            }
            
            #threadSpinBox {
                min-width: 70px;
                max-width: 70px;
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background: white;
                font-size: 14px;
            }
            
            #threadSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 5px;
            }
        """
    
    def save_config(self):
        config = {
            'urls': self.url_input.toPlainText(),
            'proxy_api': self.api_input.text(),
            'thread_count': self.thread_slider.value()
        }
        
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.log_text.append("配置已保存")
        except Exception as e:
            self.log_text.append(f"保存配置失败: {str(e)}")
            
    def load_config(self):
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                self.url_input.setPlainText(config.get('urls', ''))
                self.api_input.setText(config.get('proxy_api', ''))
                self.thread_slider.setValue(config.get('thread_count', 3))
                self.log_text.append("配置已加载")
            else:
                self.log_text.append("未找到配置文件")
        except Exception as e:
            self.log_text.append(f"加载配置失败: {str(e)}")
    
    def update_thread_status(self, value):
        """更新线程状态显示"""
        status_messages = {
            range(1, 3): "🐢 稳定模式：速度较慢但更稳定",
            range(3, 6): "👍 推荐模式：平衡的速度和稳定性",
            range(6, 8): "⚡ 快速模式：更快但可能不稳定",
            range(8, 11): "🚀 极速模式：最快但可能会出现错误"
        }
        
        for range_obj, message in status_messages.items():
            if value in range_obj:
                self.thread_status.setText(message)
                break 
    
    def parse_proxy_response(self, proxy_text):
        """解析代理响应文本"""
        try:
            # 格式: 账号:密码@代理:端口
            if '@' not in proxy_text:
                return None
                
            auth, address = proxy_text.strip().split('@')
            username_password = auth.split(':')
            host_port = address.split(':')
            
            if len(username_password) != 2 or len(host_port) != 2:
                return None
                
            username, password = username_password
            host, port = host_port
            
            return {
                'username': username,
                'password': password,
                'host': host,
                'port': port,
                'full_proxy': f"http://{username}:{password}@{host}:{port}"
            }
        except Exception as e:
            self.log_text.append(f"解析代理响应失败: {str(e)}")
            return None

    async def refresh_proxy(self):
        """刷新代理"""
        api_url = self.api_input.text().strip()
        if not api_url:
            self.log_text.append("请输入代理API链接")
            return
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url) as response:
                    if response.status == 200:
                        proxy_text = await response.text()
                        proxy_info = self.parse_proxy_response(proxy_text)
                        
                        if proxy_info:
                            self.current_proxy = proxy_info
                            self.proxy_status.setText(
                                f"当前代理: {proxy_info['host']}:{proxy_info['port']}"
                            )
                            self.log_text.append("成功更新代理")
                        else:
                            self.log_text.append("代理响应格式错误")
                    else:
                        self.log_text.append(f"获取代理失败: HTTP {response.status}")
        except Exception as e:
            self.log_text.append(f"刷新代理出错: {str(e)}")

    async def test_proxy(self):
        """测试当前代理"""
        if not hasattr(self, 'current_proxy'):
            self.log_text.append("请先获取代理")
            return
            
        try:
            async with aiohttp.ClientSession() as session:
                proxy_url = self.current_proxy['full_proxy']
                async with session.get('http://httpbin.org/ip', proxy=proxy_url) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.log_text.append(f"代理测试成功: {result.get('origin')}")
                    else:
                        self.log_text.append(f"代理测试失败: HTTP {response.status}")
        except Exception as e:
            self.log_text.append(f"代理测试出错: {str(e)}") 

    def handle_test_proxy(self):
        """处理测试代理按钮点击"""
        asyncio.run_coroutine_threadsafe(self.test_proxy(), self.loop)

    def handle_refresh_proxy(self):
        """处理刷新代理按钮点击"""
        asyncio.run_coroutine_threadsafe(self.refresh_proxy(), self.loop)

    def get_current_proxy(self):
        """获取当前代理信息"""
        if hasattr(self, 'current_proxy'):
            return self.current_proxy.get('full_proxy')
        return None 