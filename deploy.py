#!/usr/bin/env python3
"""
永续合约预测系统 - 一键部署脚本
同时启动前端和后端服务
"""

import os
import sys
import subprocess
import time
import threading
import signal
import webbrowser
from pathlib import Path

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("🚀 永续合约预测系统 - 一键部署")
    print("=" * 60)
    print("📊 支持多交易所实时数据")
    print("🤖 AI智能预测算法")
    print("💻 现代化Web界面")
    print("⚡ WebSocket实时通信")
    print("=" * 60)

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")

    # 检查Python
    try:
        import sys
        print(f"✅ Python {sys.version.split()[0]}")
    except:
        print("❌ Python未安装")
        return False

    # 检查必要的包
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("aiohttp", "AioHTTP")
    ]

    missing_packages = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} 未安装")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n📦 正在安装缺失的包: {', '.join(missing_packages)}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages,
                          check=True, capture_output=True)
            print("✅ 依赖安装完成")
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖安装失败: {e}")
            return False

    return True

def start_backend():
    """启动后端服务"""
    print("🔧 启动后端服务...")
    try:
        # 确保在backend目录运行
        backend_script = "backend/minimal_server.py"
        if not os.path.exists(backend_script):
            backend_script = "minimal_server.py"

        cmd = [sys.executable, backend_script]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        # 监控后端输出
        def monitor_backend():
            for line in iter(process.stdout.readline, ''):
                if line:
                    print(f"[后端] {line.strip()}")

        thread = threading.Thread(target=monitor_backend, daemon=True)
        thread.start()

        return process

    except Exception as e:
        print(f"❌ 后端启动失败: {e}")
        return None

def start_frontend():
    """启动前端服务"""
    print("🌐 启动前端服务...")
    try:
        # 查找可用端口
        import socket

        def find_free_port(start_port=8080):
            for port in range(start_port, start_port + 10):
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind(('localhost', port))
                        return port
                except OSError:
                    continue
            return None

        port = find_free_port()
        if not port:
            print("❌ 无法找到可用端口")
            return None, None

        cmd = [sys.executable, "-m", "http.server", str(port)]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        return process, port

    except Exception as e:
        print(f"❌ 前端启动失败: {e}")
        return None, None

def wait_for_services():
    """等待服务启动"""
    print("⏳ 等待服务启动...")

    import time
    import urllib.request
    import urllib.error

    # 等待后端服务
    backend_ready = False
    for i in range(30):  # 最多等待30秒
        try:
            urllib.request.urlopen("http://localhost:8000/health", timeout=1)
            backend_ready = True
            break
        except urllib.error.URLError:
            time.sleep(1)

    if backend_ready:
        print("✅ 后端服务已就绪")
    else:
        print("⚠️  后端服务启动超时")

    return backend_ready

def show_access_info(frontend_port):
    """显示访问信息"""
    print("\n" + "=" * 60)
    print("🎉 系统部署完成！")
    print("=" * 60)
    print("📍 访问地址:")
    print(f"  🌐 前端界面: http://localhost:{frontend_port}")
    print(f"  🔧 后端API: http://localhost:8000")
    print(f"  📚 API文档: http://localhost:8000/docs")
    print(f"  ❤️  健康检查: http://localhost:8000/health")
    print(f"  🔌 WebSocket: ws://localhost:8000/ws")
    print("\n💡 演示账号:")
    print("  📧 邮箱: demo@example.com")
    print("  🔑 密码: demo123")
    print("\n🚀 功能特性:")
    print("  📊 实时多交易所价格数据")
    print("  🤖 AI智能价格预测")
    print("  📈 可视化图表分析")
    print("  👤 用户会员管理")
    print("  🎨 明暗主题切换")
    print("\n⚠️  按 Ctrl+C 停止服务")
    print("=" * 60)

def main():
    """主函数"""
    print_banner()

    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败，请手动安装所需包")
        return 1

    # 切换到项目目录
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    try:
        # 启动后端
        backend_process = start_backend()
        if not backend_process:
            return 1

        # 等待后端启动
        if not wait_for_services():
            print("❌ 后端服务启动失败")
            return 1

        # 启动前端
        frontend_process, frontend_port = start_frontend()
        if not frontend_process:
            print("❌ 前端服务启动失败")
            return 1

        # 显示访问信息
        show_access_info(frontend_port)

        # 自动打开浏览器（可选）
        try:
            time.sleep(2)
            webbrowser.open(f"http://localhost:{frontend_port}")
        except:
            pass

        # 等待用户中断
        def signal_handler(sig, frame):
            print("\n\n🔄 正在停止服务...")
            try:
                backend_process.terminate()
                frontend_process.terminate()
                time.sleep(2)
                backend_process.kill()
                frontend_process.kill()
            except:
                pass
            print("👋 服务已停止")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        # 保持服务运行
        while True:
            if backend_process.poll() is not None:
                print("❌ 后端服务意外停止")
                break
            if frontend_process.poll() is not None:
                print("❌ 前端服务意外停止")
                break
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🔄 用户中断，正在停止服务...")
    except Exception as e:
        print(f"❌ 服务运行错误: {e}")
    finally:
        # 清理进程
        try:
            if 'backend_process' in locals():
                backend_process.terminate()
            if 'frontend_process' in locals():
                frontend_process.terminate()
        except:
            pass

    return 0

if __name__ == "__main__":
    sys.exit(main())
