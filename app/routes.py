import uuid
import os
import tempfile
import subprocess
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, send_file, current_app, url_for
import shutil

# 创建蓝图
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/generate_qsl', methods=['POST'])
def generate_qsl():
    # 生成UUID作为通讯ID
    communication_id = str(uuid.uuid4())
    
    # 获取表单数据
    # 获取表单数据（DeepSeek模型交互模拟数据 - 简化版）
    data = {
        'communication_id': communication_id,
        'model': 'deepseek-chat',
        'api_provider': 'api.deepseek.com',
        'interaction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'interaction_type': '/chat/completions',
        'input_tokens': '42',
        'output_tokens': '197',
        'quality_score': '8.9/10',
        'response_latency': '512 ms',
        'temperature': '0.7',
        'user_gpg': 'F7A3 D691 4E09 BE8C 2FDB 5A1C 3B72 8A06 D419 EF28',
        'interaction_summary': '关于中国传统节日的问答',
        'user_query': '请简要介绍一下中国的传统节日中秋节，包括它的由来和习俗。',
        'llm_response': '中秋节是中国传统的重要节日，通常在农历八月十五庆祝，以下是简要介绍：\n\n由来：\n中秋节起源于古代对月亮的崇拜和秋季丰收的庆祝活动。最早可追溯到商朝，成为固定节日则在唐代。到宋代时，中秋赏月、祭月的风俗已经很盛行。元代以后，中秋节成为与春节齐名的中国传统节日。\n\n主要习俗：\n1. 赏月：家人团聚在一起赏月，象征团圆和美好\n2. 吃月饼：月饼圆形象征团圆，是中秋节必不可少的食品\n3. 燃灯：点燃花灯或灯笼，增添节日气氛\n4. 祭月：古时有祭拜月神的习俗\n5. 猜灯谜：部分地区有猜灯谜的传统\n\n中秋节还与嫦娥奔月、吴刚伐桂等民间传说紧密相连，体现了中国人对家庭团圆的重视和对美好生活的向往。',
        'remarks': '回答准确简洁，覆盖了节日的主要历史和习俗。',
        'generation_date': datetime.now().strftime('%Y年%m月%d日')
    }
    
    # 生成HTML内容
    html_content = generate_html(data)
    
    # 使用wkhtmltopdf将HTML转换为PDF
    pdf_path = html_to_pdf(html_content)
    
    # 返回PDF文件
    return send_file(pdf_path, as_attachment=True, download_name=f"llm_qsl_{communication_id}.pdf")

def generate_html(data):
    # 读取HTML模板
    template_path = os.path.join(current_app.root_path, 'templates_html', 'qsl_template.html')
    with open(template_path, 'r', encoding='utf-8') as file:
        template = file.read()
    
    # 替换模板中的变量
    for key, value in data.items():
        template = template.replace(f'[{key}]', str(value))
    
    return template

def html_to_pdf(html_content):
    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp:
        temp.write(html_content)
        temp_path = temp.name
    
    # 调用wkhtmltopdf生成PDF
    output_path = temp_path.replace('.html', '.pdf')
    
    # 直接使用wkhtmltopdf命令
    subprocess.run([
        'wkhtmltopdf',
        '--enable-local-file-access',
        '--encoding', 'utf-8',
        '--page-size', 'A4',
        '--margin-top', '15mm',
        '--margin-right', '15mm',
        '--margin-bottom', '15mm',
        '--margin-left', '15mm',
        '--dpi', '300',
        '--print-media-type',
        '--no-background',
        '--enable-javascript',
        '--javascript-delay', '1000',
        '--disable-smart-shrinking',
        '--zoom', '1.0',
        temp_path,
        output_path
    ])
    
    # 删除临时的HTML文件
    os.remove(temp_path)
    
    return output_path

@bp.route('/preview_pdf', methods=['POST'])
def preview_pdf():
    # 生成UUID作为通讯ID
    communication_id = str(uuid.uuid4())
    
    # 获取表单数据（DeepSeek模型交互模拟数据 - 简化版）
    data = {
        'communication_id': communication_id,
        'model': 'deepseek-chat',
        'api_provider': 'api.deepseek.com',
        'interaction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
        'interaction_type': '/chat/completions',
        'input_tokens': '42',
        'output_tokens': '197',
        'quality_score': '8.9/10',
        'response_latency': '512 ms',
        'temperature': '0.7',
        'user_gpg': 'F7A3 D691 4E09 BE8C 2FDB 5A1C 3B72 8A06 D419 EF28',
        'interaction_summary': '关于中国传统节日的问答',
        'user_query': '请简要介绍一下中国的传统节日中秋节，包括它的由来和习俗。',
        'llm_response': '中秋节是中国传统的重要节日，通常在农历八月十五庆祝，以下是简要介绍：\n\n由来：\n中秋节起源于古代对月亮的崇拜和秋季丰收的庆祝活动。最早可追溯到商朝，成为固定节日则在唐代。到宋代时，中秋赏月、祭月的风俗已经很盛行。元代以后，中秋节成为与春节齐名的中国传统节日。\n\n主要习俗：\n1. 赏月：家人团聚在一起赏月，象征团圆和美好\n2. 吃月饼：月饼圆形象征团圆，是中秋节必不可少的食品\n3. 燃灯：点燃花灯或灯笼，增添节日气氛\n4. 祭月：古时有祭拜月神的习俗\n5. 猜灯谜：部分地区有猜灯谜的传统\n\n中秋节还与嫦娥奔月、吴刚伐桂等民间传说紧密相连，体现了中国人对家庭团圆的重视和对美好生活的向往。',
        'remarks': '回答准确简洁，覆盖了节日的主要历史和习俗。',
        'generation_date': datetime.now().strftime('%Y年%m月%d日')
    }
    
    # 生成HTML内容
    html_content = generate_html(data)
    
    # 使用wkhtmltopdf将HTML转换为PDF
    pdf_path = html_to_pdf(html_content)
    
    # 将PDF保存到静态目录
    static_pdf_path = os.path.join(current_app.root_path, 'static', 'previews', f"preview_{communication_id}.pdf")
    os.makedirs(os.path.dirname(static_pdf_path), exist_ok=True)
    
    shutil.copy(pdf_path, static_pdf_path)
    
    # 删除临时PDF文件
    os.remove(pdf_path)
    
    # 返回预览URL
    preview_url = url_for('static', filename=f"previews/preview_{communication_id}.pdf")
    return jsonify({'preview_url': preview_url})
