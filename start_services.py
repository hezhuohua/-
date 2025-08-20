#!/usr/bin/env python3
"""
简化的服务启动脚本
"""

import os
import sys
import time
import threading
import http.server
import socketserver
from pathlib import Path

def create_secure_env():
    """创建安全的环境配置"""
    if os.path.exists(".env"):
        print("✓ .env文件已存在")
        return
    
    import secrets
    import string
    
    # 生成安全的SECRET_KEY
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(64))
    
    env_content = f"""# 安全配置
SECRET_KEY={secret_key}
CSRF_SECRET_KEY={secrets.token_urlsafe(32)}
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# 数据库配置
DATABASE_URL=sqlite:///./crypto_prediction.db

# Redis配置（可选）
REDIS_URL=redis://localhost:6379

# API配置
DEEPSEEK_API_KEY=demo-key-for-testing

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=True
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_content)
    print("✓ 创建安全的.env配置文件")

def setup_directories():
    """创建必要目录"""
    dirs = ["uploads", "uploads/qrcodes", "uploads/proofs", "static", "logs"]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    print("✓ 创建必要目录")

def start_frontend_server():
    """启动前端HTTP服务器"""
    try:
        PORT = 8080
        Handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"✓ 前端服务启动: http://localhost:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"前端服务启动失败: {e}")

def start_backend_server():
    """启动后端服务"""
    try:
        # 设置环境变量
        os.environ.setdefault("PYTHONPATH", os.getcwd())
        
        # 导入FastAPI应用
        sys.path.insert(0, os.path.join(os.getcwd(), "backend"))
        
        from backend.main import app
        import uvicorn
        
        print("✓ 后端服务启动: http://localhost:8000")
        print("✓ API文档地址: http://localhost:8000/docs")
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所需依赖: pip install fastapi uvicorn")
    except Exception as e:
        print(f"后端服务启动失败: {e}")

def main():
    """主函数"""
    print("🚀 永续合约预测系统 - 快速启动")
    print("=" * 50)
    
    # 创建配置和目录
    create_secure_env()
    setup_directories()
    
    print("\n📋 服务信息:")
    print("- 前端界面: http://localhost:8080")
    print("- 后端API: http://localhost:8000")
    print("- API文档: http://localhost:8000/docs")
    
    try:
        # 启动前端服务（后台线程）
        frontend_thread = threading.Thread(target=start_frontend_server, daemon=True)
        frontend_thread.start()
        
        # 等待前端服务启动
        time.sleep(1)
        
        # 启动后端服务（主线程）
        start_backend_server()
        
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print("\n🔧 故障排除:")
        print("1. 检查Python环境是否正确")
        print("2. 安装依赖: pip install fastapi uvicorn python-dotenv")
        print("3. 检查端口8000和8080是否被占用")

if __name__ == "__main__":
    main()
