@echo off
chcp 65001 >nul
echo 🚀 永续合约预测系统启动器
echo ================================

echo 📋 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    echo 请安装Python 3.8+并添加到系统PATH
    pause
    exit /b 1
)

echo ✅ Python环境正常

echo 📦 检查依赖...
python -c "import fastapi, uvicorn" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 缺少必要依赖，正在安装...
    python -m pip install fastapi uvicorn python-dotenv
    if errorlevel 1 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

echo ✅ 依赖检查完成

echo 🔧 创建必要目录...
if not exist "uploads" mkdir uploads
if not exist "uploads\qrcodes" mkdir uploads\qrcodes
if not exist "uploads\proofs" mkdir uploads\proofs
if not exist "static" mkdir static
if not exist "logs" mkdir logs

echo 🔑 检查环境配置...
if not exist ".env" (
    echo 正在创建.env配置文件...
    python -c "
import secrets
import string
alphabet = string.ascii_letters + string.digits + '!@#$%%^&*'
secret_key = ''.join(secrets.choice(alphabet) for _ in range(64))
env_content = f'''SECRET_KEY={secret_key}
CSRF_SECRET_KEY={secrets.token_urlsafe(32)}
ACCESS_TOKEN_EXPIRE_MINUTES=43200
DATABASE_URL=sqlite:///./crypto_prediction.db
REDIS_URL=redis://localhost:6379
DEEPSEEK_API_KEY=demo-key-for-testing
HOST=0.0.0.0
PORT=8000
DEBUG=True
LOG_LEVEL=INFO
LOG_FILE=logs/app.log'''
with open('.env', 'w') as f:
    f.write(env_content)
print('✅ 创建.env配置文件')
"
)

echo 🌐 启动前端服务（后台）...
start /B python -m http.server 8080 >nul 2>&1

echo ⏳ 等待前端服务启动...
timeout /t 2 >nul

echo 🚀 启动后端服务...
echo 📍 服务地址:
echo   - 前端界面: http://localhost:8080
echo   - 后端API: http://localhost:8000  
echo   - API文档: http://localhost:8000/docs
echo   - 健康检查: http://localhost:8000/health
echo.
echo 💡 演示账号: demo@example.com / demo123
echo ⚠️ 按 Ctrl+C 停止服务
echo.

python backend/minimal_server.py

echo.
echo 👋 服务已停止
pause
