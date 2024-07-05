import requests

def fetch_text_bychatgpt(text,api_key,model):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': model,
         "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text}
    ]
    }
    # 发送POST请求到OpenAI的API
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data
    )
    # 检查响应状态码
    if response.status_code == 200:
        # 解析响应数据
        completion = response.json()
        generated_text = completion['choices'][0]['message']['content'].strip()
        return generated_text
    else:
        return ""

    