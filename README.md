# 英文词频统计助手

一个基于 Python + PyQt5 的英语文本词频分析工具，支持批量处理文本文件、停用词过滤、图表生成和数据导出功能。

## 🚀 功能特点

- ✅ **批量文件处理**: 支持读取指定目录下所有 `.txt` 文件
- ✅ **智能文本处理**: 自动清洗文本、分词、去除停用词
- ✅ **词频统计**: 精确统计词汇出现频率并排序
- ✅ **图表可视化**: 支持柱状图和词云图展示
- ✅ **数据导出**: 将结果导出为 CSV 格式
- ✅ **图形界面**: 简洁直观的 PyQt5 用户界面
- ✅ **自定义停用词**: 支持加载自定义停用词表
- 🔄 **词性过滤**: 预留接口，便于后续扩展

## 📦 环境要求

- Python 3.8+
- PyQt5
- NLTK
- matplotlib
- wordcloud

## 🛠️ 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd EnglishWordFrequencyAnalyzer
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **下载 NLTK 数据**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## 🎯 使用方法

### 方法一：图形界面启动
```bash
python main.py
```

### 方法二：命令行测试各模块
```bash
# 测试文件加载器
python analyzer/file_loader.py

# 测试文本处理器
python analyzer/text_processor.py

# 测试词频统计器
python analyzer/counter.py

# 测试CSV导出器
python exporter/csv_exporter.py

# 测试图表生成
python visualization/plot_bar.py
python visualization/wordcloud_gen.py
```

## 📖 使用指南

### 1. 启动程序
运行 `python main.py` 启动图形界面

### 2. 选择文本文件夹
点击"浏览"按钮，选择包含 `.txt` 文件的文件夹

### 3. 设置停用词（可选）
如需使用自定义停用词，点击停用词文件的"浏览"按钮选择文件

### 4. 开始分析
点击"开始分析"按钮，程序将自动：
- 加载所有txt文件
- 清洗和处理文本
- 统计词频
- 显示结果

### 5. 查看结果
- **词频结果** 选项卡：显示前100个高频词汇
- **统计信息** 选项卡：显示详细的统计数据

### 6. 导出和可视化
- **导出CSV**: 将词频数据保存为CSV文件
- **生成图表**: 显示柱状图（垂直和水平）
- **生成词云**: 创建词云图

## 📁 项目结构

```
EnglishWordFrequencyAnalyzer/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
├── word_freq_tech_doc.md  # 技术文档
├── analyzer/              # 文本分析核心模块
│   ├── __init__.py
│   ├── file_loader.py     # 文件加载器
│   ├── text_processor.py  # 文本处理器
│   ├── counter.py         # 词频统计器
│   ├── pos_filter.py      # 词性过滤器（预留）
│   └── stopwords.py       # 停用词管理（预留）
├── visualization/         # 可视化模块
│   ├── __init__.py
│   ├── plot_bar.py        # 柱状图生成器
│   └── wordcloud_gen.py   # 词云生成器
└── exporter/             # 数据导出模块
    ├── __init__.py
    └── csv_exporter.py    # CSV导出器
```

## 🔧 自定义配置

### 停用词文件格式
创建一个文本文件，每行一个停用词：
```
the
and
of
to
in
...
```

### 修改显示数量
在 `main.py` 中可以调整：
- 结果表格显示行数（默认100行）
- 图表显示词汇数量（柱状图20个，词云100个）

## ⚠️ 注意事项

1. **文件编码**: 程序优先使用UTF-8编码读取文件，如失败会尝试GBK编码
2. **内存占用**: 处理大量文件时可能占用较多内存
3. **NLTK数据**: 首次运行需要下载NLTK相关数据包
4. **词性过滤**: 当前版本暂未启用，但保留了接口

## 🐛 故障排除

### 问题1: NLTK数据下载失败
```bash
# 手动下载
python -c "import nltk; nltk.download('punkt', download_dir='~/nltk_data')"
python -c "import nltk; nltk.download('stopwords', download_dir='~/nltk_data')"
```

### 问题2: PyQt5安装问题
```bash
# 如果pip安装失败，尝试conda
conda install pyqt
```

### 问题3: 中文显示问题
程序界面支持中文，如遇显示问题请检查系统字体配置。