from flask import Flask, request, Response
import requests

app = Flask(__name__)

# 捕获所有路径
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    target_url = request.headers.get('Target-Url')
    
    # 【排错专用】如果你在浏览器直接打开 https://pai.yingziai.cn，会走到这里
    if not target_url:
        return "Proxy is running! 代理服务运行正常，请通过代码携带 Target-Url 请求。", 200

    # 清洗掉 Vercel 自身的 Header，保留其他 Header
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ['host', 'target-url']}

    try:
        # Vercel 免费版最大超时是 10 秒，设为 9 秒防止 Vercel 抛出 504 页面
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

# 本地调试用
if __name__ == '__main__':
    app.run(port=8080)
