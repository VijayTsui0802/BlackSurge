from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QTextEdit, QLineEdit, QSpinBox, QSlider, QRadioButton, QButtonGroup, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

def create_title_section():
    """创建标题区域"""
    title_frame = QFrame()
    title_frame.setObjectName("titleFrame")
    title_layout = QHBoxLayout(title_frame)
    
    title_label = QLabel("代理IP网站访问工具")
    title_label.setObjectName("titleLabel")
    
    version_label = QLabel("v1.0")
    version_label.setObjectName("versionLabel")
    
    title_layout.addWidget(title_label)
    title_layout.addStretch()
    title_layout.addWidget(version_label)
    
    return title_frame

def create_url_section():
    """创建URL输入区域"""
    url_frame = QFrame()
    url_frame.setObjectName("inputFrame")
    url_layout = QVBoxLayout(url_frame)
    
    url_header = QLabel("URLs (每行一个):")
    url_header.setObjectName("sectionHeader")
    
    url_desc = QLabel("格式：网址----访问次数\n例如：https://mail.tm/zh/----1000")
    url_desc.setObjectName("descLabel")
    
    url_input = QTextEdit()
    url_input.setPlaceholderText("请输入要访问的网址\n例如：https://mail.tm/zh/----1000")
    url_input.setMinimumHeight(150)
    
    url_layout.addWidget(url_header)
    url_layout.addWidget(url_desc)
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

def create_main_content(proxy_manager):
    """创建主要内容区域（左右布局）"""
    content_frame = QFrame()
    content_layout = QHBoxLayout(content_frame)
    content_layout.setSpacing(20)
    
    # 左侧面板
    left_panel = QFrame()
    left_layout = QVBoxLayout(left_panel)
    left_layout.setSpacing(15)
    
    # URL输入区域
    url_frame, url_input = create_url_section()
    left_layout.addWidget(url_frame)
    
    # 代理设置区域
    proxy_frame = create_proxy_section(proxy_manager)
    left_layout.addWidget(proxy_frame)
    
    # 浏览器模式选择
    mode_frame, mode_group = create_browser_mode_section()
    left_layout.addWidget(mode_frame)
    
    left_layout.addStretch()
    
    # 右侧面板
    right_panel = QFrame()
    right_layout = QVBoxLayout(right_panel)
    right_layout.setSpacing(15)
    
    # 访问控制区域
    control_frame, min_time_input, max_time_input, min_interval_input, max_interval_input, thread_slider, start_btn, stop_btn, save_btn, load_btn = create_control_section()
    right_layout.addWidget(control_frame)
    
    # 日志显示区域
    log_frame, log_text = create_log_section()
    right_layout.addWidget(log_frame, stretch=1)
    
    # 添加到主布局
    content_layout.addWidget(left_panel)
    content_layout.addWidget(right_panel)
    content_layout.setStretch(0, 4)
    content_layout.setStretch(1, 6)
    
    return (
        content_frame, 
        url_input, 
        mode_group, 
        log_text,
        min_time_input,
        max_time_input,
        min_interval_input,
        max_interval_input,
        thread_slider,
        start_btn,
        stop_btn,
        save_btn,
        load_btn
    )

def create_control_section():
    """创建访问控制区域"""
    control_frame = QFrame()
    control_frame.setObjectName("controlFrame")
    control_layout = QVBoxLayout(control_frame)
    control_layout.setSpacing(15)
    
    # 时间控制
    time_group = QGroupBox("访问时间控制")
    time_group.setObjectName("controlGroup")
    time_layout = QVBoxLayout(time_group)
    time_layout.setSpacing(10)
    
    time_desc = QLabel("设置每个网页的停留时间范围")
    time_desc.setObjectName("descLabel")
    time_layout.addWidget(time_desc)
    
    time_input_layout = QHBoxLayout()
    time_input_layout.setSpacing(20)
    
    # 最小时间
    min_time_layout = QVBoxLayout()
    min_time_label = QLabel("最小时间")
    min_time_label.setObjectName("controlLabel")
    min_time_input = QSpinBox()
    min_time_input.setRange(1, 300)
    min_time_input.setValue(10)
    min_time_input.setSuffix(" 秒")
    min_time_input.setObjectName("timeSpinBox")
    min_time_input.setMinimumWidth(120)  # 设置最小宽度
    min_time_input.setFixedHeight(30)    # 设置固定高度
    min_time_layout.addWidget(min_time_label)
    min_time_layout.addWidget(min_time_input)
    
    # 最大时间
    max_time_layout = QVBoxLayout()
    max_time_label = QLabel("最大时间")
    max_time_label.setObjectName("controlLabel")
    max_time_input = QSpinBox()
    max_time_input.setRange(1, 300)
    max_time_input.setValue(20)
    max_time_input.setSuffix(" 秒")
    max_time_input.setObjectName("timeSpinBox")
    max_time_input.setMinimumWidth(120)  # 设置最小宽度
    max_time_input.setFixedHeight(30)    # 设置固定高度
    max_time_layout.addWidget(max_time_label)
    max_time_layout.addWidget(max_time_input)
    
    time_input_layout.addLayout(min_time_layout)
    time_input_layout.addLayout(max_time_layout)
    time_input_layout.addStretch()  # 添加弹性空间
    time_layout.addLayout(time_input_layout)
    
    # 间隔时间控制
    interval_group = QGroupBox("访问间隔控制")
    interval_group.setObjectName("controlGroup")
    interval_layout = QVBoxLayout(interval_group)
    interval_layout.setSpacing(10)
    
    interval_desc = QLabel("设置两次访问之间的间隔时间范围")
    interval_desc.setObjectName("descLabel")
    interval_layout.addWidget(interval_desc)
    
    interval_input_layout = QHBoxLayout()
    interval_input_layout.setSpacing(20)
    
    # 最小间隔时间
    min_interval_layout = QVBoxLayout()
    min_interval_label = QLabel("最小间隔")
    min_interval_label.setObjectName("controlLabel")
    min_interval_input = QSpinBox()
    min_interval_input.setRange(0, 3600)  # 0秒到1小时
    min_interval_input.setValue(5)
    min_interval_input.setSuffix(" 秒")
    min_interval_input.setObjectName("timeSpinBox")
    min_interval_input.setMinimumWidth(120)
    min_interval_input.setFixedHeight(30)
    min_interval_layout.addWidget(min_interval_label)
    min_interval_layout.addWidget(min_interval_input)
    
    # 最大间隔时间
    max_interval_layout = QVBoxLayout()
    max_interval_label = QLabel("最大间隔")
    max_interval_label.setObjectName("controlLabel")
    max_interval_input = QSpinBox()
    max_interval_input.setRange(0, 3600)
    max_interval_input.setValue(15)
    max_interval_input.setSuffix(" 秒")
    max_interval_input.setObjectName("timeSpinBox")
    max_interval_input.setMinimumWidth(120)
    max_interval_input.setFixedHeight(30)
    max_interval_layout.addWidget(max_interval_label)
    max_interval_layout.addWidget(max_interval_input)
    
    interval_input_layout.addLayout(min_interval_layout)
    interval_input_layout.addLayout(max_interval_layout)
    interval_input_layout.addStretch()
    interval_layout.addLayout(interval_input_layout)
    
    # 线程控制
    thread_group = QGroupBox("并发控制")
    thread_group.setObjectName("controlGroup")
    thread_layout = QVBoxLayout(thread_group)
    thread_layout.setSpacing(10)
    
    thread_desc = QLabel("设置同时访问的网站数量")
    thread_desc.setObjectName("descLabel")
    
    thread_slider = QSlider(Qt.Orientation.Horizontal)
    thread_slider.setRange(1, 10)
    thread_slider.setValue(3)
    thread_slider.setObjectName("threadSlider")
    thread_slider.setFixedHeight(30)  # 设置固定高度
    
    thread_value_layout = QHBoxLayout()
    thread_value_label = QLabel("当前数量:")
    thread_value_label.setObjectName("controlLabel")
    thread_value = QLabel("3")
    thread_value.setObjectName("valueLabel")
    thread_value.setMinimumWidth(30)  # 设置最小宽度
    thread_slider.valueChanged.connect(lambda v: thread_value.setText(str(v)))
    
    thread_value_layout.addWidget(thread_value_label)
    thread_value_layout.addWidget(thread_value)
    thread_value_layout.addStretch()
    
    thread_layout.addWidget(thread_desc)
    thread_layout.addWidget(thread_slider)
    thread_layout.addLayout(thread_value_layout)
    
    # 按钮区域
    button_layout = QHBoxLayout()
    button_layout.setSpacing(10)
    
    # 操作按钮组
    operation_layout = QHBoxLayout()
    start_btn = QPushButton("开始访问")
    start_btn.setObjectName("primaryButton")
    start_btn.setIcon(QIcon("icons/start.png"))  # 如果有图标的话
    
    stop_btn = QPushButton("停止访问")
    stop_btn.setObjectName("dangerButton")
    stop_btn.setIcon(QIcon("icons/stop.png"))  # 如果有图标的话
    
    operation_layout.addWidget(start_btn)
    operation_layout.addWidget(stop_btn)
    
    # 配置按钮组
    config_layout = QHBoxLayout()
    save_btn = QPushButton("保存配置")
    save_btn.setObjectName("secondaryButton")
    
    load_btn = QPushButton("加载配置")
    load_btn.setObjectName("secondaryButton")
    
    config_layout.addWidget(save_btn)
    config_layout.addWidget(load_btn)
    
    button_layout.addLayout(operation_layout)
    button_layout.addStretch()
    button_layout.addLayout(config_layout)
    
    # 组装控制区域
    control_layout.addWidget(time_group)
    control_layout.addWidget(interval_group)
    control_layout.addWidget(thread_group)
    control_layout.addLayout(button_layout)
    
    return (
        control_frame, 
        min_time_input, 
        max_time_input, 
        min_interval_input,
        max_interval_input,
        thread_slider, 
        start_btn, 
        stop_btn, 
        save_btn, 
        load_btn
    )

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

def create_browser_mode_section():
    """创建浏览器模式选择区域"""
    mode_frame = QFrame()
    mode_frame.setObjectName("inputFrame")
    mode_layout = QVBoxLayout(mode_frame)
    
    mode_header = QLabel("浏览器模式")
    mode_header.setObjectName("sectionHeader")
    
    mode_desc = QLabel("选择浏览器运行模式")
    mode_desc.setObjectName("descLabel")
    
    # 创建单选按钮
    headless_radio = QRadioButton("无头模式（后台运行）")
    visible_radio = QRadioButton("可见模式（显示浏览器）")
    visible_radio.setChecked(True)  # 默认选择可见模式
    
    # 创建按钮组
    mode_group = QButtonGroup()
    mode_group.addButton(headless_radio)
    mode_group.addButton(visible_radio)
    
    # 组装布局
    mode_layout.addWidget(mode_header)
    mode_layout.addWidget(mode_desc)
    mode_layout.addWidget(visible_radio)
    mode_layout.addWidget(headless_radio)
    
    return mode_frame, mode_group 