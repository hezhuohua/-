@echo off
chcp 65001 >nul
title 永续合约预测系统 - 通用启动器

echo.
echo ========================================
echo    🚀 永续合约预测系统启动器
echo ========================================
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python环境检查通过

:: 检查依赖是否安装
echo.
echo 📦 检查Python依赖...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo ⚠️  检测到缺少依赖，正在安装...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo ✅ 依赖安装完成
) else (
    echo ✅ 依赖检查通过
)

echo.
echo 🚀 启动后端服务...
echo 📊 服务地址: http://localhost:5000
echo 🌐 前端地址: http://localhost:8080/index.html
echo.

:: 启动后端服务
start "永续合约预测系统后端" python start_server.py

:: 等待3秒让后端启动
timeout /t 3 /nobreak >nul

:: 启动前端服务
echo 🌐 启动前端服务...
start "永续合约预测系统前端" python -m http.server 8080

echo.
echo ✅ 系统启动完成！
echo.
echo 📋 使用说明:
echo 1. 后端API服务运行在: http://localhost:5000
echo 2. 前端界面访问: http://localhost:8080/index.html
echo 3. 请确保币安API Key已正确配置
echo 4. 建议先使用测试网络熟悉系统
echo.
echo ⚠️  重要提醒:
echo - 请确保API Key仅勾选"交易"和"查询"权限
echo - 禁止提现权限，确保资金安全
echo - 建议设置IP白名单限制
echo.
echo 按任意键退出...
pause >nul
