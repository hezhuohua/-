#!/usr/bin/env python3
"""
永续合约预测系统启动脚本
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def check_requirements():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import redis
        import sqlalchemy
        print("✓ 依赖检查通过")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def setup_directories():
    """创建必要的目录"""
    directories = [
        "uploads",
        "uploads/qrcodes",
        "uploads/proofs",
        "static",
        "logs"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def create_env_file():
    """创建环境配置文件"""
    import secrets
    import string

    # 生成安全的SECRET_KEY
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(64))

    env_content = f"""# 安全配置 - 自动生成的安全密钥
SECRET_KEY={secret_key}
CSRF_SECRET_KEY={secrets.token_urlsafe(32)}
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# 数据库配置
DATABASE_URL=sqlite:///./crypto_prediction.db

# Redis配置
REDIS_URL=redis://localhost:6379

# DEEPSEEK API配置（可选）
DEEPSEEK_API_KEY=demo-key-for-testing

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=True

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""

    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✓ 创建环境配置文件 .env")
    else:
        print("✓ 环境配置文件已存在")

def start_redis():
    """启动Redis服务（如果需要）"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        print("✓ Redis服务已运行")
        return True
    except:
        print("⚠ Redis服务未运行，某些功能可能受限")
        return False

def create_demo_data():
    """创建演示数据"""
    print("✓ 初始化演示数据...")

    # 这里可以添加创建演示用户、收款码等数据的代码
    demo_script = """
from backend.database import SessionLocal, engine
from backend.models import Base, User, PaymentQRCode
from backend.auth import get_password_hash
from datetime import datetime

# 创建数据库表
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 创建演示用户
demo_user = db.query(User).filter(User.email == "demo@example.com").first()
if not demo_user:
    demo_user = User(
        username="demo_user",
        email="demo@example.com",
        password_hash=get_password_hash("demo123"),
        membership_level="trial",
        trial_start_time=datetime.now()
    )
    db.add(demo_user)
    db.commit()
    print("创建演示用户: demo@example.com / demo123")

# 创建演示收款码
demo_qrcode = db.query(PaymentQRCode).first()
if not demo_qrcode:
    demo_qrcode = PaymentQRCode(
        payment_type="alipay",
        qrcode_url="/static/demo_qrcode.png",
        qrcode_name="演示收款码",
        status="active"
    )
    db.add(demo_qrcode)
    db.commit()
    print("创建演示收款码")

db.close()
print("演示数据初始化完成")
"""

    try:
        exec(demo_script)
    except Exception as e:
        print(f"⚠ 演示数据创建失败: {e}")

def start_backend():
    """启动后端服务"""
    print("🚀 启动后端服务...")

    # 切换到backend目录
    os.chdir("backend")

    try:
        # 启动FastAPI服务
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n后端服务已停止")
    except Exception as e:
        print(f"启动后端服务失败: {e}")

def start_frontend():
    """启动前端服务"""
    print("🌐 前端服务地址: http://localhost:8080")

    try:
        # 使用Python内置HTTP服务器
        subprocess.run([
            sys.executable, "-m", "http.server", "8080"
        ])
    except KeyboardInterrupt:
        print("\n前端服务已停止")

def main():
    """主函数"""
    print("=" * 50)
    print("🚀 永续合约预测系统启动器")
    print("=" * 50)

    # 检查依赖
    if not check_requirements():
        return

    # 设置目录
    setup_directories()

    # 创建配置文件
    create_env_file()

    # 检查Redis
    start_redis()

    # 创建演示数据
    create_demo_data()

    print("\n" + "=" * 50)
    print("✅ 系统初始化完成")
    print("=" * 50)

    print("\n📋 服务信息:")
    print("- 后端API: http://localhost:8000")
    print("- 前端界面: http://localhost:8080")
    print("- API文档: http://localhost:8000/docs")
    print("- 演示账号: demo@example.com / demo123")

    print("\n🎯 使用说明:")
    print("1. 打开浏览器访问 http://localhost:8080")
    print("2. 点击右上角登录，使用演示账号登录")
    print("3. 体验交易仪表盘和AI预测功能")
    print("4. 查看会员中心了解收费模式")

    print("\n⚠️  注意事项:")
    print("- 当前使用模拟数据，实际部署需要配置真实API")
    print("- Redis服务可选，不影响基本功能演示")
    print("- 按 Ctrl+C 停止服务")

    print("\n" + "=" * 50)

    try:
        # 在后台启动前端服务
        frontend_thread = threading.Thread(target=start_frontend)
        frontend_thread.daemon = True
        frontend_thread.start()

        # 等待一下让前端服务启动
        time.sleep(2)

        # 启动后端服务（主线程）
        start_backend()

    except KeyboardInterrupt:
        print("\n\n👋 系统已停止，感谢使用！")

if __name__ == "__main__":
    main()
