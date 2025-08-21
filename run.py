#!/usr/bin/env python3
"""
永续合约预测系统启动脚本
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import redis
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_redis():
    """检查Redis是否运行"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✅ Redis服务正在运行")
        return True
    except Exception:
        print("⚠️  Redis服务未运行，将使用内存缓存")
        return False

def create_directories():
    """创建必要的目录"""
    dirs = ['logs', 'uploads', 'static']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ 目录结构已创建")

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ 后端目录不存在")
        return False

    try:
        # 切换到后端目录
        os.chdir(backend_dir)

        # 启动FastAPI服务
        cmd = [
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ]

        print(f"执行命令: {' '.join(cmd)}")
        process = subprocess.Popen(cmd)

        # 等待服务启动
        time.sleep(3)

        # 检查服务是否启动成功
        try:
            import requests
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ 后端服务启动成功")
                return process
            else:
                print("❌ 后端服务启动失败")
                return None
        except Exception as e:
            print(f"❌ 后端服务检查失败: {e}")
            return None

    except Exception as e:
        print(f"❌ 启动后端服务失败: {e}")
        return None

def start_frontend():
    """启动前端服务"""
    print("🎨 启动前端服务...")
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ 前端目录不存在")
        return False

    try:
        # 切换到前端目录
        os.chdir(frontend_dir)

        # 启动Dash应用
        cmd = [sys.executable, "app.py"]
        print(f"执行命令: {' '.join(cmd)}")
        process = subprocess.Popen(cmd)

        # 等待服务启动
        time.sleep(3)

        print("✅ 前端服务启动成功")
        return process

    except Exception as e:
        print(f"❌ 启动前端服务失败: {e}")
        return None

def open_browser():
    """打开浏览器"""
    print("🌐 打开浏览器...")
    try:
        # 等待服务完全启动
        time.sleep(5)

        # 打开前端页面
        webbrowser.open("http://localhost:8080")

        # 打开API文档
        webbrowser.open("http://localhost:8000/docs")

        print("✅ 浏览器已打开")
    except Exception as e:
        print(f"❌ 打开浏览器失败: {e}")

def main():
    """主函数"""
    print("🚀 永续合约预测系统启动中...")
    print("=" * 50)

    # 检查依赖
    if not check_dependencies():
        return

    # 检查Redis
    check_redis()

    # 创建目录
    create_directories()

    # 启动后端
    backend_process = start_backend()
    if not backend_process:
        print("❌ 无法启动后端服务")
        return

    # 启动前端
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ 无法启动前端服务")
        backend_process.terminate()
        return

    print("\n🎉 系统启动成功！")
    print("=" * 50)
    print("📱 前端界面: http://localhost:8080")
    print("🔧 后端API: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("=" * 50)
    print("按 Ctrl+C 停止服务")

    # 打开浏览器
    open_browser()

    try:
        # 等待用户中断
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")

        # 停止前端
        if frontend_process:
            frontend_process.terminate()
            print("✅ 前端服务已停止")

        # 停止后端
        if backend_process:
            backend_process.terminate()
            print("✅ 后端服务已停止")

        print("👋 服务已停止，再见！")

if __name__ == "__main__":
    main()
