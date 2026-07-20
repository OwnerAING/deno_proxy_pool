from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    target_url = request.headers.get('Target-Url')
    if not target_url:
        return "Missing Target-Url header", 400

    # 清洗掉 Vercel 自身的 Header，伪装成直接请求
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'target-url']}

    try:
        # Vercel 免费版最大超时 10s，我们设为 9s 防止 Vercel 抛出丑陋的 504 页面
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            allow_redirects=True,
            timeout=9 
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        response_headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, response_headers)
    
    except requests.exceptions.Timeout:
        return "Proxy Timeout", 504
    except Exception as e:
        return str(e), 500
