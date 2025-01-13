from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from ui_components import (
    create_title_section,
    create_main_content,
)
from proxy_manager import ProxyManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("代理IP网站访问器")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self.get_style_sheet())
        
        # 创建代理管理器
        self.proxy_manager = ProxyManager(self)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 0, 20, 20)
        
        # 添加标题
        main_layout.addWidget(create_title_section())
        
        # 创建主要内容（左右布局）
        (
            content_frame, 
            self.url_input, 
            self.browser_mode_group, 
            self.log_text,
            self.min_time_input,
            self.max_time_input,
            self.thread_slider,
            self.start_btn,
            self.stop_btn,
            self.save_btn,
            self.load_btn
        ) = create_main_content(self.proxy_manager)
        main_layout.addWidget(content_frame)
        
        # 连接信号
        self.save_btn.clicked.connect(self.proxy_manager.save_config)
        self.load_btn.clicked.connect(self.proxy_manager.load_config)
        self.url_input.textChanged.connect(self.auto_save_config)
        self.proxy_manager.proxy_input.textChanged.connect(self.auto_save_config)
        self.thread_slider.valueChanged.connect(self.auto_save_config)
        self.min_time_input.valueChanged.connect(self.auto_save_config)
        self.max_time_input.valueChanged.connect(self.auto_save_config)
        self.browser_mode_group.buttonClicked.connect(self.auto_save_config)
        
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
            QMainWindow {
                background-color: #f5f6fa;
            }
            
            QFrame {
                background-color: transparent;
            }
            
            #titleFrame {
                background-color: #2c3e50;
                padding: 10px;
                border-radius: 0px;
            }
            
            #titleLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            
            #versionLabel {
                color: #bdc3c7;
                font-size: 14px;
            }
            
            #inputFrame, #controlFrame {
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                border: 1px solid #e0e0e0;
            }
            
            QGroupBox {
                font-weight: bold;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin-top: 1ex;
                padding: 10px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            
            #sectionHeader {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            
            #descLabel {
                color: #7f8c8d;
                margin-bottom: 5px;
            }
            
            QTextEdit, QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            
            QTextEdit:focus, QLineEdit:focus {
                border-color: #3498db;
            }
            
            #primaryButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 100px;
            }
            
            #primaryButton:hover {
                background-color: #2980b9;
            }
            
            #dangerButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 100px;
            }
            
            #dangerButton:hover {
                background-color: #c0392b;
            }
            
            #secondaryButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 100px;
            }
            
            #secondaryButton:hover {
                background-color: #7f8c8d;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #bdc3c7;
                height: 8px;
                background: #e0e0e0;
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #3498db;
                border: none;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            
            QSpinBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
            }
            
            QRadioButton {
                spacing: 8px;
            }
            
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            
            #controlGroup {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin-top: 8px;
                padding: 15px;
            }
            
            #controlLabel {
                color: #2c3e50;
                font-weight: bold;
                font-size: 13px;
            }
            
            #valueLabel {
                color: #3498db;
                font-weight: bold;
                font-size: 14px;
            }
            
            #timeSpinBox {
                padding: 5px 10px;
                min-width: 120px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
                background-color: white;
            }
            
            #timeSpinBox::up-button, #timeSpinBox::down-button {
                width: 20px;
                background-color: #f0f0f0;
                border: none;
                border-left: 1px solid #bdc3c7;
            }
            
            #timeSpinBox::up-button:hover, #timeSpinBox::down-button:hover {
                background-color: #e0e0e0;
            }
            
            #threadSlider {
                height: 30px;
                margin: 10px 0;
            }
            
            #threadSlider::groove:horizontal {
                border: 1px solid #bdc3c7;
                height: 10px;
                background: #e0e0e0;
                margin: 0px;
                border-radius: 5px;
            }
            
            #threadSlider::handle:horizontal {
                background: #3498db;
                border: none;
                width: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
            
            #threadSlider::handle:horizontal:hover {
                background: #2980b9;
            }
            
            #valueLabel {
                color: #3498db;
                font-weight: bold;
                font-size: 14px;
                min-width: 30px;
                padding: 0 5px;
            }
            
            QGroupBox {
                font-size: 14px;
            }
        """
        
    def closeEvent(self, event):
        self.proxy_manager.close()
        event.accept() 
        
    def auto_save_config(self):
        """自动保存配置"""
        self.proxy_manager.save_config(show_message=False) 
        
    def get_current_proxy(self):
        """获取当前代理信息的代理方法"""
        return self.proxy_manager.get_current_proxy() 
        
    def get_time_range(self):
        """获取访问时间范围设置"""
        return {
            'min_time': self.min_time_input.value(),
            'max_time': self.max_time_input.value()
        } 
        
    def get_browser_mode(self):
        """获取浏览器模式设置"""
        return self.browser_mode_group.checkedButton().text() == "无头模式（后台运行）" 