# 基于Flask框架的抖音电商热点数据可视化分析系统

## 项目简介

本系统基于Python + Flask + Selenium框架，实现抖音电商热点数据的爬取、存储与可视化分析。

## 环境配置

### 1. 创建虚拟环境
```bash
# Windows
python -m venv douyin_env
douyin_env\Scripts\activate.bat

# 或直接运行配置脚本
setup_env.bat
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 下载ChromeDriver

**重要：请根据您的Chrome浏览器版本下载对应的ChromeDriver**

#### 下载地址：
- **官方地址**: https://chromedriver.chromium.org/downloads
- **新版地址**: https://googlechromelabs.github.io/chrome-for-testing/

#### 安装步骤：
1. 打开Chrome浏览器，地址栏输入：`chrome://version/`
2. 查看版本号（如：143.0.7499.170）
3. 下载对应版本的ChromeDriver
4. 将 `chromedriver.exe` 放在 `driver` 目录下

## 项目结构

```
douyin_analysis/
├── crawler.py          # 数据爬虫模块
├── app.py              # Flask Web应用（待开发）
├── requirements.txt    # 依赖包列表
├── setup_env.bat       # 环境配置脚本(Windows)
├── README.md           # 项目说明
├── driver/             # ChromeDriver目录
│   └── chromedriver.exe
├── data/               # 数据存储目录（待创建）
├── templates/          # Flask模板目录（待创建）
└── static/             # 静态资源目录（待创建）
```

## 使用方法

### 运行爬虫
```bash
douyin_env\Scripts\python.exe crawler.py
```

## 开发进度

### 爬虫模块
- [x] **步骤1**: 虚拟环境配置与基础依赖安装
- [x] **步骤2**: Selenium基础环境搭建
- [ ] **步骤3**: 目标URL访问与页面加载验证
- [ ] **步骤4**: 数据定位（XPath/CSS选择器编写）
- [ ] **步骤5**: 数据提取与格式化
- [ ] **步骤6**: 数据存储
- [ ] **步骤7**: 异常处理与稳定性优化
- [ ] **步骤8**: 代码封装与可复用性优化

### Flask Web模块（待开发）
- [ ] Flask应用框架搭建
- [ ] 数据可视化页面
- [ ] 热点数据分析功能
- [ ] 图表展示（ECharts/Plotly）

## 注意事项

1. 确保Chrome浏览器已安装
2. ChromeDriver版本必须与Chrome浏览器版本匹配
3. 目标网站可能有反爬机制，请合理设置请求间隔
4. 遵守网站robots.txt和使用条款