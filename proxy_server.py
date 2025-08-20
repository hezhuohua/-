#!/usr/bin/env python3
"""
简单的代理服务器 - 将API请求从8080转发到8000端口
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import json
from http import HTTPStatus

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """处理POST请求，转发到后端API"""
        if self.path.startswith('/api/'):
            # 转发API请求到后端
            try:
                # 读取请求体
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)

                # 构建转发请求
                backend_url = f"http://localhost:8000{self.path}"
                req = urllib.request.Request(backend_url, data=post_data)
                req.add_header('Content-Type', 'application/json')
                req.add_header('Content-Length', str(len(post_data)))

                # 发送请求到后端
                with urllib.request.urlopen(req) as response:
                    response_data = response.read()

                # 返回响应
                self.send_response(HTTPStatus.OK)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(response_data)

            except Exception as e:
                print(f"代理错误: {e}")
                self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = json.dumps({"error": "代理服务器错误", "detail": str(e)})
                self.wfile.write(error_response.encode())
        else:
            # 其他请求按原样处理
            super().do_POST()

    def do_OPTIONS(self):
        """处理CORS预检请求"""
        self.send_response(HTTPStatus.OK)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def end_headers(self):
        """添加CORS头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    PORT = 8080
    print(f"🚀 启动代理服务器在端口 {PORT}")
    print(f"📡 API请求将转发到 http://localhost:8000")

    with socketserver.TCPServer(("", PORT), ProxyHTTPRequestHandler) as httpd:
        print(f"✅ 代理服务器已启动: http://localhost:{PORT}")
        print("按 Ctrl+C 停止服务器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 服务器已停止")
