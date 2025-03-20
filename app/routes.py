import uuid
import os
import tempfile
import subprocess
from datetime import datetime
from flask import render_template, request, jsonify, send_file, current_app, url_for
from app import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qsl', methods=['POST'])
def generate_qsl():
    # 生成UUID作为通讯ID
    communication_id = str(uuid.uuid4())
    
    # 获取表单数据
    data = {
        'communication_id': communication_id,
        'model': request.form.get('model', 'gpt-4-turbo'),
        'api_provider': request.form.get('api_provider', 'openai.com'),
        'interaction_time': request.form.get('interaction_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')),
        'interaction_type': request.form.get('interaction_type', '/chat/completions'),
        'input_tokens': request.form.get('input_tokens', '350'),
        'output_tokens': request.form.get('output_tokens', '620'),
        'quality_score': request.form.get('quality_score', '9.2/10'),
        'response_latency': request.form.get('response_latency', '1250 ms'),
        'temperature': request.form.get('temperature', '0.7'),
        'user_gpg': request.form.get('user_gpg', 'ABCD 1234 5678 EFGH 9012 3456 7890 IJKL'),
        'interaction_summary': request.form.get('interaction_summary', '关于LLM交互QSL卡片设计的讨论'),
        'user_query': request.form.get('user_query', '请帮我设计一个LLM交互QSL卡片的生成器...'),
        'llm_response': request.form.get('llm_response', '基于传统QSL卡片和发票设计，我建议您的LLM交互卡片包含以下字段...'),
        'remarks': request.form.get('remarks', '')
    }
    
    # 生成LaTeX内容
    latex_content = generate_latex(data)
    
    # 使用Pandoc将LaTeX转换为PDF
    pdf_path = latex_to_pdf(latex_content)
    
    # 返回PDF文件
    return send_file(pdf_path, as_attachment=True, download_name=f"llm_qsl_{communication_id}.pdf")

def generate_latex(data):
    # 读取LaTeX模板
    template_path = os.path.join(current_app.root_path, 'templates_latex', 'qsl_template.tex')
    with open(template_path, 'r', encoding='utf-8') as file:
        template = file.read()
    
    # 替换模板中的变量
    for key, value in data.items():
        template = template.replace(f'[{key}]', str(value))
    
    return template

def latex_to_pdf(latex_content):
    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.tex', delete=False, mode='w', encoding='utf-8') as temp:
        temp.write(latex_content)
        temp_path = temp.name
    
    # 调用Pandoc生成PDF
    output_path = temp_path.replace('.tex', '.pdf')
    subprocess.run(['pandoc', temp_path, '-o', output_path, '--pdf-engine=xelatex'])
    
    # 删除临时的.tex文件
    os.remove(temp_path)
    
    return output_path

@app.route('/preview_pdf', methods=['POST'])
def preview_pdf():
    # 生成UUID作为通讯ID
    communication_id = str(uuid.uuid4())
    
    # 获取表单数据
    data = {
        'communication_id': communication_id,
        'model': request.form.get('model', 'gpt-4-turbo'),
        'api_provider': request.form.get('api_provider', 'openai.com'),
        'interaction_time': request.form.get('interaction_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')),
        'interaction_type': request.form.get('interaction_type', '/chat/completions'),
        'input_tokens': request.form.get('input_tokens', '350'),
        'output_tokens': request.form.get('output_tokens', '620'),
        'quality_score': request.form.get('quality_score', '9.2/10'),
        'response_latency': request.form.get('response_latency', '1250 ms'),
        'temperature': request.form.get('temperature', '0.7'),
        'user_gpg': request.form.get('user_gpg', 'ABCD 1234 5678 EFGH 9012 3456 7890 IJKL'),
        'interaction_summary': request.form.get('interaction_summary', '关于LLM交互QSL卡片设计的讨论'),
        'user_query': request.form.get('user_query', '请帮我设计一个LLM交互QSL卡片的生成器...'),
        'llm_response': request.form.get('llm_response', '基于传统QSL卡片和发票设计，我建议您的LLM交互卡片包含以下字段...'),
        'remarks': request.form.get('remarks', '')
    }
    
    # 生成LaTeX内容
    latex_content = generate_latex(data)
    
    # 使用Pandoc将LaTeX转换为PDF
    pdf_path = latex_to_pdf(latex_content)
    
    # 将PDF保存到静态目录
    static_pdf_dir = os.path.join(current_app.root_path, 'static', 'pdf')
    os.makedirs(static_pdf_dir, exist_ok=True)
    
    static_pdf_path = os.path.join(static_pdf_dir, f"llm_qsl_{communication_id}.pdf")
    os.rename(pdf_path, static_pdf_path)
    
    # 返回PDF的URL
    pdf_url = url_for('static', filename=f'pdf/llm_qsl_{communication_id}.pdf')
    return jsonify({'pdf_url': pdf_url})

if __name__ == '__main__':
    app.run(debug=True)
