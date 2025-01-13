from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from ui_components import (
    create_title_section,
    create_url_section,
    create_proxy_section,
    create_time_section,
    create_thread_section,
    create_button_section,
    create_log_section
)
from proxy_manager import ProxyManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("代理IP网站访问器")
        self.setGeometry(100, 100, 1000, 800)
        self.setStyleSheet(self.get_style_sheet())
        
        # 创建代理管理器
        self.proxy_manager = ProxyManager(self)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加各个部分
        main_layout.addWidget(create_title_section())
        main_layout.addWidget(self.create_separator())
        
        # URL输入区域
        url_frame, self.url_input = create_url_section()
        main_layout.addWidget(url_frame)
        
        # 代理设置区域
        proxy_frame = create_proxy_section(self.proxy_manager)
        main_layout.addWidget(proxy_frame)
        
        # 访问时间控制区域
        time_frame, self.min_time_input, self.max_time_input = create_time_section()
        main_layout.addWidget(time_frame)
        
        # 线程控制区域
        thread_frame, self.thread_slider = create_thread_section()
        main_layout.addWidget(thread_frame)
        
        # 按钮区域
        button_frame, self.start_btn, self.stop_btn, self.save_btn, self.load_btn = create_button_section()
        main_layout.addWidget(button_frame)
        
        # 日志显示区域
        log_frame, self.log_text = create_log_section()
        main_layout.addWidget(log_frame)
        
        # 连接信号
        self.save_btn.clicked.connect(self.proxy_manager.save_config)
        self.load_btn.clicked.connect(self.proxy_manager.load_config)
        self.url_input.textChanged.connect(self.auto_save_config)
        self.proxy_manager.proxy_input.textChanged.connect(self.auto_save_config)
        self.thread_slider.valueChanged.connect(self.auto_save_config)
        self.min_time_input.valueChanged.connect(self.auto_save_config)
        self.max_time_input.valueChanged.connect(self.auto_save_config)
        
        # 自动加载配置
        self.proxy_manager.load_config()
        
    def create_separator(self):
        from PyQt6.QtWidgets import QFrame
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator
        
    def get_style_sheet(self):
        return """
            /* 样式定义保持不变 */
        """
        
    def closeEvent(self, event):
        self.proxy_manager.close()
        event.accept() 
        
    def auto_save_config(self):
        """自动保存配置"""
        self.proxy_manager.save_config(show_message=False) 