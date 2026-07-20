from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    target_url = request.headers.get('Target-Url')
    
    # 浏览器直接访问的提示
    if not target_url:
        return "Proxy is running! 代理部署成功！请在代码中携带 Target-Url 请求。", 200

    # 清除 Vercel 附加的请求头
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'target-url']}

    try:
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
