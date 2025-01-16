# 代理IP网站访问工具 🌐

<div align="center">

![GitHub release (latest by date)](https://img.shields.io/github/v/release/yourusername/proxy-ip-tool)
![GitHub](https://img.shields.io/github/license/yourusername/proxy-ip-tool)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![PyQt Version](https://img.shields.io/badge/PyQt-6.0%2B-green)
![Playwright](https://img.shields.io/badge/Playwright-latest-orange)

</div>

## 📝 项目介绍

一个基于 PyQt6 和 Playwright 的代理 IP 访问工具，支持多线程、自定义时间间隔的网站自动化访问工具。本工具适用于网站测试、性能分析等场景。

## ✨ 功能特点

- 🔄 支持批量输入待访问的 URL 和访问次数
- 🌍 支持自定义代理服务器设置
- ⏱️ 自定义访问时间和间隔
- 🚀 多线程并发访问
- 🎯 支持有头/无头浏览器模式
- 💾 自动保存配置信息
- 📊 实时显示访问状态和日志
- 🛡️ 内置异常处理机制
- 📈 访问数据统计和导出

## 🛠️ 安装说明

### 系统要求

- Python 3.8 或更高版本
- Windows/Linux/MacOS 操作系统

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/proxy-ip-tool.git
cd proxy-ip-tool
```

2. 安装依赖
```bash
pip install -r requirements.txt
playwright install
```

## 🚀 使用说明

### 快速开始

1. 运行主程序
```bash
python main.py
```

2. 在主界面配置以下参数：
   - URL列表
   - 代理设置
   - 访问间隔
   - 线程数量
   - 浏览器模式

### URL 格式要求

- 每行一个URL
- 支持HTTP和HTTPS协议
- 格式示例：
```
https://example.com
http://example.org
```

### 代理设置格式

支持以下格式：
```
http://username:password@host:port
socks5://host:port
```

## ⚙️ 配置说明

### 基础配置
- `config.json`: 保存基本配置信息
- `proxy_list.txt`: 代理服务器列表
- `urls.txt`: 目标URL列表

### 高级配置
- 浏览器参数设置
- 网络超时设置
- 并发控制
- 日志级别

## 📊 数据导出

支持以下格式导出访问数据：
- CSV
- JSON
- Excel

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📝 更新日志

### [1.0.8] - 2024-03-27
- 🔧 修复：解决异步资源关闭问题
- 🛠️ 优化：改进事件循环管理机制
- 🧹 优化：完善资源清理流程
- 🚀 优化：提升多线程稳定性

### [1.0.7] - 2024-03-27
- ✨ 新增功能：每个线程随机访问不同网站
- 🔒 优化线程安全：添加线程锁保护URL列表访问
- 🎯 防重复访问：确保每个URL只被访问一次
- 🚀 性能优化：优化了线程资源管理和释放机制

### 标签创建和推送
```bash
git tag v1.0.7
git push origin v1.0.7
```

### [1.0.0] - 2024-01-01
- 初始版本发布
- 基础功能实现

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🤔 常见问题

1. Q: 如何处理代理连接失败？
   A: 系统会自动重试并切换到备用代理

2. Q: 支持哪些浏览器？
   A: 支持 Chromium、Firefox 和 WebKit

## 📞 联系方式

- 项目作者：[Your Name]
- 邮箱：[your.email@example.com]
- GitHub：[@yourusername](https://github.com/yourusername)

## 🌟 致谢

感谢以下开源项目：
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- [Playwright](https://playwright.dev/) 