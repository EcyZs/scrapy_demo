

```markdown
# 新华网 AI 新闻采集与可视化分析系统

一个使用 Python 实现的自动化新闻数据采集与趋势分析项目，基于 [新华网](http://www.xinhuanet.com) 的关键词搜索结果，爬取“AI”相关新闻，提取标题、时间、来源和正文内容，并进行数据清洗与可视化展示。

## 📌 项目结构

```
```bash
│  main.py          # 主程序：爬取新闻并保存为 JSON和CSV
│  test.py          # 测试脚本：验证爬虫功能正确性
│  test2.py
│
├─DATA
│      news.csv     # 爬取后的CSV数据（程序自动生成）
│      news.json    # 爬取后的json数据（程序自动生成）
│
└─可视化
        main_vis.py  # 可视化模块：读取 CSV 并绘图展示

```



````

## 🛠️ 技术栈

- `requests`：发送网页请求
- `lxml`：解析网页并提取信息（XPath）
- `pandas`：处理表格数据
- `matplotlib`：生成可视化图表

## 🚀 使用方法

### 1. 安装依赖

确保已安装 Python 3.7 及以上版本，然后安装必要库：

```bash
pip install requests lxml pandas matplotlib
````

### 2. 运行爬虫

```bash
python main.py
```

* 程序会自动分页抓取新华网中包含“AI”关键词的新闻；
* 输出数据保存为 `result.csv` 文件。

### 3. 生成可视化图表

```bash
python main_vis.py
```

* 程序将读取 `result.csv`；
* 输出每日新闻数量折线图，保存为 `output.png`。

### 4. 运行测试

```bash
python test.py
```

* 执行基本测试，确保链接解析、数据抽取功能正常。


## ✅ 功能特点

* 自动分页爬取搜索结果，避免遗漏新闻；
* 使用 XPath 精确提取新闻各字段内容；
* 数据清洗、格式统一、结构良好；
* 可视化展示关键词相关新闻趋势，支持扩展分析；
* 模块划分清晰，具备基础测试能力。

## 📦 可扩展方向

* 由于访问过慢，可以使用多线程或多协程提速
* 支持多关键词输入和更多新闻源；
* 接入数据库存储与搜索；
* 增加情感分析、词频分析等文本处理；
* 部署为网页可交互应用（如 Streamlit）。

## 📄 License

本项目仅供学习与研究用途，禁止用于任何商业目的。如涉及爬取网站的权限问题，请遵守对应网站的 [robots.txt](http://www.xinhuanet.com/robots.txt) 和法律规定。

