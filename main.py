from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = "sat_4jWrb0q5Q45x3RAXERS3VNfuj98vPlgNUvPwsmRzYJOTzStATo4dAW5lTaWsRBx8"

@app.route('/solve-multi', methods=['POST'])
def solve():
    data = request.json
    urls = data.get('imageUrls', [])
    task = data.get('task', '')
    
    if len(urls) < 6:
        return jsonify({'error': 'Need 6 URLs'})
    
    content = [{"type": "text", "text": f"Task: {task}\n\nSelect 2 matching images. Output only numbers like '1,3'."}]
    for url in urls[:6]:
        content.append({"type": "image_url", "image_url": {"url": url, "detail": "high"}})
    
    payload = {
        "model": "doubao-seed-1-6-vision-250815",
        "messages": [{"role": "user", "content": content}],
        "temperature": 0.3
    }
    
    resp = requests.post(
        'https://api.coze.cn/v3/chat',
        json=payload,
        headers={'Authorization': f'Bearer {API_KEY}'},
        timeout=120
    )
    
    result = resp.json()
    if result.get('code') == 0:
        text = result.get('data', {}).get('messages', [{}])[0].get('content', '')
        answer = ''.join(c for c in text if c.isdigit() or c == ',')
        return jsonify({'answer': answer})
    else:
        return jsonify({'error': result.get('msg')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))