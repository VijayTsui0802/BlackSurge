from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QLineEdit, QSpinBox, QSlider
)
from PyQt6.QtCore import Qt

def create_title_section():
    title_label = QLabel("代理IP网站访问工具")
    title_label.setObjectName("titleLabel")
    return title_label

def create_url_section():
    """创建URL输入区域"""
    url_frame = QFrame()
    url_frame.setObjectName("inputFrame")
    url_layout = QVBoxLayout(url_frame)
    
    url_header = QLabel("URLs (每行一个):")
    url_header.setObjectName("sectionHeader")
    url_input = QTextEdit()
    url_input.setPlaceholderText("请输入要访问的网址，每行一个")
    url_input.setMinimumHeight(150)
    
    url_layout.addWidget(url_header)
    url_layout.addWidget(url_input)
    
    return url_frame, url_input

def create_proxy_section(proxy_manager):
    proxy_frame = QFrame()
    proxy_frame.setObjectName("inputFrame")
    proxy_layout = QVBoxLayout(proxy_frame)
    
    # 代理设置组件
    proxy_header = QLabel("代理设置")
    proxy_header.setObjectName("sectionHeader")
    
    proxy_desc = QLabel("格式: 服务器:端口:用户名格式:密码 (用{sid}表示会话ID)")
    proxy_desc.setObjectName("descLabel")
    
    proxy_input = QLineEdit()
    proxy_input.setPlaceholderText("例如: prem.iprocket.io:9595:com23112818-res-BR-sid-{sid}-sesstime-5:ZvXa2ey06FmX41o1tLcY")
    proxy_manager.proxy_input = proxy_input
    
    proxy_status = QLabel("当前未设置代理")
    proxy_status.setObjectName("proxyStatus")
    proxy_manager.proxy_status = proxy_status
    
    test_btn = QPushButton("测试代理")
    test_btn.setObjectName("primaryButton")
    test_btn.setMinimumWidth(120)
    test_btn.setMinimumHeight(35)
    test_btn.clicked.connect(proxy_manager.handle_test_proxy)
    
    # 组装布局
    proxy_layout.addWidget(proxy_header)
    proxy_layout.addWidget(proxy_desc)
    proxy_layout.addWidget(proxy_input)
    proxy_layout.addWidget(proxy_status)
    proxy_layout.addWidget(test_btn)
    
    return proxy_frame

def create_time_section():
    """创建访问时间控制区域"""
    time_frame = QFrame()
    time_frame.setObjectName("inputFrame")
    time_layout = QVBoxLayout(time_frame)
    
    time_header = QLabel("访问时间控制")
    time_header.setObjectName("sectionHeader")
    time_desc = QLabel("设置每个网页的停留时间范围（秒）")
    time_desc.setObjectName("descLabel")
    
    # 时间范围输入布局
    time_range_layout = QHBoxLayout()
    
    # 最小时间
    min_time_layout = QVBoxLayout()
    min_time_label = QLabel("最小时间(秒)")
    min_time_label.setObjectName("controlLabel")
    min_time_input = QSpinBox()
    min_time_input.setRange(1, 300)
    min_time_input.setValue(10)
    min_time_input.setObjectName("timeSpinBox")
    min_time_layout.addWidget(min_time_label)
    min_time_layout.addWidget(min_time_input)
    
    # 最大时间
    max_time_layout = QVBoxLayout()
    max_time_label = QLabel("最大时间(秒)")
    max_time_label.setObjectName("controlLabel")
    max_time_input = QSpinBox()
    max_time_input.setRange(1, 300)
    max_time_input.setValue(20)
    max_time_input.setObjectName("timeSpinBox")
    max_time_layout.addWidget(max_time_label)
    max_time_layout.addWidget(max_time_input)
    
    # 添加到时间范围布局
    time_range_layout.addLayout(min_time_layout)
    time_range_layout.addLayout(max_time_layout)
    
    # 组装时间控制布局
    time_layout.addWidget(time_header)
    time_layout.addWidget(time_desc)
    time_layout.addLayout(time_range_layout)
    
    return time_frame, min_time_input, max_time_input

def create_thread_section():
    """创建线程控制区域"""
    thread_frame = QFrame()
    thread_frame.setObjectName("inputFrame")
    thread_layout = QVBoxLayout(thread_frame)
    
    thread_header = QLabel("线程控制")
    thread_header.setObjectName("sectionHeader")
    thread_desc = QLabel("调整同时访问的网站数量 (建议: 3-5个)")
    thread_desc.setObjectName("descLabel")
    
    # 滑块布局
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
    thread_slider = QSlider(Qt.Orientation.Horizontal)
    thread_slider.setRange(1, 10)
    thread_slider.setValue(3)
    thread_slider.setObjectName("threadSlider")
    
    # 添加到布局
    slider_layout.addWidget(min_label)
    slider_layout.addWidget(thread_slider)
    slider_layout.addWidget(max_label)
    
    # 组装布局
    thread_layout.addWidget(thread_header)
    thread_layout.addWidget(thread_desc)
    thread_layout.addLayout(slider_layout)
    
    return thread_frame, thread_slider

def create_button_section():
    """创建按钮区域"""
    button_frame = QFrame()
    button_frame.setObjectName("buttonFrame")
    button_layout = QHBoxLayout(button_frame)
    
    start_btn = QPushButton("开始访问")
    start_btn.setObjectName("primaryButton")
    
    stop_btn = QPushButton("停止访问")
    stop_btn.setObjectName("dangerButton")
    
    save_btn = QPushButton("保存配置")
    save_btn.setObjectName("primaryButton")
    
    load_btn = QPushButton("加载配置")
    load_btn.setObjectName("primaryButton")
    
    # 统一按钮大小
    for btn in [start_btn, stop_btn, save_btn, load_btn]:
        btn.setMinimumWidth(120)
        btn.setMinimumHeight(35)
    
    button_layout.addWidget(start_btn)
    button_layout.addWidget(stop_btn)
    button_layout.addStretch()
    button_layout.addWidget(save_btn)
    button_layout.addWidget(load_btn)
    
    return button_frame, start_btn, stop_btn, save_btn, load_btn

def create_log_section():
    """创建日志显示区域"""
    log_frame = QFrame()
    log_frame.setObjectName("inputFrame")
    log_layout = QVBoxLayout(log_frame)
    
    log_header = QLabel("运行日志")
    log_header.setObjectName("sectionHeader")
    
    log_text = QTextEdit()
    log_text.setReadOnly(True)
    log_text.setMinimumHeight(200)
    
    log_layout.addWidget(log_header)
    log_layout.addWidget(log_text)
    
    return log_frame, log_text 