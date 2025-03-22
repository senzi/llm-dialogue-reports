import os
import json
import uuid
import time
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.deepseek.com",
)

system_prompt = """
你现在处于JSON模式，请帮助用户回答问题，但回复必须控制在500字以内。你的回复必须是有效的JSON格式，包含以下字段：

1. answer (string): 对用户问题的简明回答，不超过500字
2. summary (string): 用一句话概括此次交互的核心内容，不超过30字
3. quality_score (number): 给本次对话的质量评分，1-100之间的整数，请基于用户提问的有趣性以及你回答的准确性、简洁性和帮助性评分综合评分
4. remarks (string): 对用户的提问进行一句话犀利吐槽，不超过50字

你必须严格按照这个JSON结构回复，不要在JSON外添加任何文本。例如：

{
  "answer": "你的简明回答，不超过500字",
  "summary": "交互内容概括，不超过30字",
  "quality_score": 80,
  "remarks": "对用户提问的一句话犀利吐槽"
}

无论问题如何，请确保包含所有字段并保持格式正确。
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    start_time = time.time()
    
    # 获取用户输入
    user_id = request.form.get('username')
    user_query = request.form.get('question')
    
    # 生成会话ID
    communication_id = str(uuid.uuid4())
    
    # 准备API调用
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
    
    try:
        # 调用API
        print(f"正在调用API，用户: {user_id}, 问题: {user_query}")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            response_format={'type': 'json_object'}
        )
        print(f"API调用完成，状态码: {response.model_dump().get('object')}")
        
        # 计算响应时间
        response_latency = round((time.time() - start_time) * 1000)  # 转换为毫秒
        
        # 解析响应
        response_content = response.choices[0].message.content
        print(f"API返回内容: {response_content}")
        llm_response = json.loads(response_content)
        
        # 生成对话哈希
        conversation_text = user_query + llm_response['answer']
        conversation_hash = hashlib.sha256(conversation_text.encode()).hexdigest().upper()
        
        # 准备返回数据
        result = {
            'communication_id': communication_id,
            'interaction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'api_provider': 'Deepseek',
            'model': 'deepseek-chat',
            'input_tokens': response.usage.prompt_tokens,
            'output_tokens': response.usage.completion_tokens,
            'temperature': 0.7,  # 默认值
            'response_latency': response_latency,
            'user_id': user_id,
            'user_query': user_query,
            'llm_response': llm_response.get('answer', ''),
            'interaction_summary': llm_response.get('summary', ''),
            'quality_score': llm_response.get('quality_score', 0),
            'remarks': llm_response.get('remarks', ''),
            'conversation_hash': conversation_hash,
            'generation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return render_template('result.html', **result)
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
