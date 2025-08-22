@echo off
chcp 65001 >nul
title 永续合约预测系统启动器

echo 🚀 永续合约预测系统启动器
echo ================================
echo.

echo 🔍 检查系统环境...
echo.

:: 检查Python
echo 检查Python安装...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo ✅ %PYTHON_VERSION%
) else (
    echo ❌ Python未找到
    echo.
    echo 请安装Python 3.8或更高版本:
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装Python
    echo 3. 安装时请勾选"添加Python到PATH"
    echo.
    pause
    exit /b 1
)

:: 检查项目文件
echo.
echo 检查项目文件...
if exist "index.html" (
    echo ✅ index.html 文件存在
) else (
    echo ❌ index.html 文件不存在
    pause
    exit /b 1
)

if exist "backend" (
    echo ✅ backend 目录存在
) else (
    echo ❌ backend 目录不存在
    pause
    exit /b 1
)

:: 安装依赖
echo.
echo 📦 检查并安装依赖...
pip install fastapi uvicorn >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 依赖安装完成
) else (
    echo ⚠️ 依赖安装失败（可能已安装或无网络）
)

:: 启动后端服务
echo.
echo 🚀 启动后端服务...
cd backend
start "后端服务" /min python minimal_server.py
cd ..

:: 等待后端服务启动
echo ⏳ 等待后端服务启动...
timeout /t 5 >nul

:: 启动前端服务
echo.
echo 🌐 启动前端服务...
start "前端服务" /min python -m http.server 8080

:: 等待前端服务启动
echo ⏳ 等待前端服务启动...
timeout /t 5 >nul

:: 打开浏览器
echo.
echo 🖥️ 打开系统页面...
start "" "http://localhost:8080/index.html"

:: 显示服务信息
echo.
echo 📋 系统信息:
echo   - 前端界面: http://localhost:8080/index.html
echo   - 后端API: http://localhost:8000
echo   - API文档: http://localhost:8000/docs
echo   - 演示账号: demo@example.com / demo123

echo.
echo ✅ 系统启动完成！
echo ⚠️ 如页面未自动打开，请手动访问: http://localhost:8080/index.html
echo ⚠️ 按任意键关闭此窗口（服务将继续在后台运行）
pause >nul