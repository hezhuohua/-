#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
移动端访问服务器
让手机和其他设备可以访问您的永续合约预测系统
"""

import http.server
import socketserver
import socket
import webbrowser
import os
import sys
from pathlib import Path

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 创建一个socket连接来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def start_server(port=8080):
    """启动HTTP服务器"""
    
    # 确保在正确的目录
    current_dir = Path(__file__).parent
    os.chdir(current_dir)
    
    # 检查index.html是否存在
    if not os.path.exists("index.html"):
        print("❌ 错误：找不到index.html文件")
        print("请确保在项目根目录运行此脚本")
        return
    
    # 获取本机IP
    local_ip = get_local_ip()
    
    # 自定义HTTP处理器，支持CORS
    class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            super().end_headers()
        
        def do_OPTIONS(self):
            self.send_response(200)
            self.end_headers()
    
    # 启动服务器
    try:
        with socketserver.TCPServer(("", port), CORSHTTPRequestHandler) as httpd:
            print("🚀 永续合约预测系统移动端服务器启动成功！")
            print("=" * 60)
            print(f"📱 本机访问地址：http://localhost:{port}")
            print(f"📱 手机访问地址：http://{local_ip}:{port}")
            print("=" * 60)
            print("📋 使用说明：")
            print("1. 确保手机和电脑连接同一个WiFi")
            print("2. 在手机浏览器输入上面的手机访问地址")
            print("3. 其他人也可以用这个地址访问")
            print("4. 按 Ctrl+C 停止服务器")
            print("=" * 60)
            
            # 自动打开浏览器
            try:
                webbrowser.open(f"http://localhost:{port}")
                print("✅ 已自动打开浏览器")
            except:
                print("⚠️  请手动打开浏览器访问")
            
            print(f"🌐 服务器运行在端口 {port}...")
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 10048:  # 端口被占用
            print(f"❌ 端口 {port} 被占用，尝试使用端口 {port + 1}")
            start_server(port + 1)
        else:
            print(f"❌ 启动服务器失败：{e}")
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")

if __name__ == "__main__":
    print("🎯 永续合约预测系统 - 移动端服务器")
    print("让您的手机和其他设备都能访问系统")
    print()
    
    # 检查命令行参数
    port = 8080
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("⚠️  端口号必须是数字，使用默认端口8080")
    
    start_server(port)
