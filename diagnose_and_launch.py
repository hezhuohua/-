#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统诊断和启动脚本
"""

import os
import sys
import subprocess
import webbrowser
import time
import socket
from pathlib import Path

def check_port(port):
    """检查端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def find_python():
    """查找Python可执行文件"""
    python_paths = [
        sys.executable,
        'python',
        'python3',
        '/usr/bin/python',
        '/usr/bin/python3',
        'C:\\Python\\python.exe',
        'C:\\Python39\\python.exe',
        'C:\\Python38\\python.exe'
    ]
    
    for path in python_paths:
        try:
            result = subprocess.run([path, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return path
        except:
            continue
    return None

def start_server(command, port, name):
    """启动服务器"""
    try:
        print(f"🚀 启动{name}...")
        process = subprocess.Popen(command, shell=True)
        time.sleep(3)  # 等待服务器启动
        
        # 检查端口是否被占用（表示服务器已启动）
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) == 0:
                print(f"✅ {name}已启动 (端口: {port})")
                return process
            else:
                print(f"⚠️  {name}启动可能失败")
                return process
    except Exception as e:
        print(f"❌ 启动{name}失败: {e}")
        return None

def main():
    print("🔍 永续合约预测系统诊断工具")
    print("=" * 50)
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"📁 当前目录: {current_dir}")
    
    # 检查必需文件
    required_files = ['index.html', 'NEW.HTML']
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ 找到文件: {file}")
        else:
            print(f"❌ 缺少文件: {file}")
    
    # 查找Python
    python_exe = find_python()
    if python_exe:
        print(f"✅ Python路径: {python_exe}")
        
        # 获取Python版本
        try:
            result = subprocess.run([python_exe, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            print(f"✅ Python版本: {result.stdout.strip()}")
        except Exception as e:
            print(f"⚠️  无法获取Python版本: {e}")
    else:
        print("❌ 未找到Python，请确保已安装Python并添加到PATH")
        return
    
    # 检查依赖
    try:
        import fastapi
        print("✅ FastAPI已安装")
    except ImportError:
        print("⚠️  FastAPI未安装，某些功能可能受限")
    
    try:
        import uvicorn
        print("✅ Uvicorn已安装")
    except ImportError:
        print("⚠️  Uvicorn未安装，后端服务可能无法启动")
    
    # 启动后端服务
    backend_dir = os.path.join(current_dir, 'backend')
    if os.path.exists(backend_dir):
        os.chdir(backend_dir)
        backend_cmd = f'"{python_exe}" minimal_server.py'
        backend_process = start_server(backend_cmd, 8000, "后端服务")
        os.chdir(current_dir)  # 切换回原目录
    else:
        print("❌ 未找到backend目录")
        backend_process = None
    
    # 启动前端服务
    frontend_cmd = f'"{python_exe}" -m http.server 8080'
    frontend_process = start_server(frontend_cmd, 8080, "前端服务")
    
    # 等待服务启动
    time.sleep(5)
    
    # 检查服务状态
    services = [
        (8000, "后端API", "http://localhost:8000"),
        (8080, "前端界面", "http://localhost:8080/index.html"),
        (8000, "API文档", "http://localhost:8000/docs")
    ]
    
    print("\n📋 服务状态检查:")
    print("-" * 30)
    for port, name, url in services:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) == 0:
                    print(f"✅ {name}: {url} (运行中)")
                else:
                    print(f"❌ {name}: {url} (未运行)")
        except Exception as e:
            print(f"❌ {name}: {url} (检查失败: {e})")
    
    # 打开浏览器
    print("\n🌐 尝试打开浏览器...")
    urls = [
        "http://localhost:8080/index.html",
        "http://localhost:8000",
        "http://localhost:8000/docs"
    ]
    
    for url in urls:
        try:
            webbrowser.open(url)
            print(f"✅ 已打开: {url}")
            time.sleep(1)  # 间隔1秒打开下一个
        except Exception as e:
            print(f"❌ 无法打开 {url}: {e}")
    
    print("\n💡 使用说明:")
    print("- 演示账号: demo@example.com / demo123")
    print("- 如页面无法打开，请检查防火墙设置")
    print("- 按 Ctrl+C 可停止所有服务")
    
    # 保持服务运行
    try:
        if frontend_process or backend_process:
            print("\n⏳ 服务运行中... 按 Ctrl+C 停止")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        if frontend_process:
            frontend_process.terminate()
        if backend_process:
            backend_process.terminate()
        print("✅ 服务已停止")

if __name__ == "__main__":
    main()