# LLM对话报告生成器

基于Flask、Pandoc和LaTeX的LLM交互QSL卡片生成器，用于生成和打印与LLM对话的报告，专注于布局设计和API集成。

## 功能特点

- 生成类似发票风格的LLM交互QSL卡片
- 支持A4纸张打印
- 提供Web界面进行数据输入和预览
- 使用LaTeX模板确保高质量排版
- 通过Pandoc将LaTeX转换为PDF

## 安装要求

1. Python 3.7+
2. Flask
3. Pandoc
4. LaTeX (推荐使用XeLaTeX)
5. LaTeX包：geometry, array, booktabs, longtable, graphicx, fancyhdr, xcolor, tabularx, tikz, qrcode, fontspec

## 安装步骤

1. 克隆仓库：
   ```
   git clone https://github.com/yourusername/llm-dialogue-reports.git
   cd llm-dialogue-reports
   ```

2. 安装Python依赖：
   ```
   pip install -r requirements.txt
   ```

3. 安装Pandoc和LaTeX（如果尚未安装）：
   - macOS: `brew install pandoc texlive`
   - Ubuntu: `sudo apt-get install pandoc texlive-full`
   - Windows: 下载并安装[Pandoc](https://pandoc.org/installing.html)和[MiKTeX](https://miktex.org/download)

## 使用方法

1. 启动Flask应用：
   ```
   python run.py
   ```

2. 在浏览器中访问：`http://127.0.0.1:5000`

3. 填写表单并点击"预览QSL卡片"或"下载QSL卡片"

## 自定义

- 修改`app/templates_latex/qsl_template.tex`以更改PDF布局
- 调整`app/static/css/styles.css`以更改Web界面样式
