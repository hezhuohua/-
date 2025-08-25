@echo off
chcp 65001 >nul
title 简化依赖安装器

echo.
echo ========================================
echo   🎯 简化依赖安装器
echo ========================================
echo.

echo 📦 正在安装核心依赖包（跳过需要编译的包）...
echo.

:: 升级pip
python -m pip install --upgrade pip

:: 安装核心依赖（不需要编译）
echo 1. 安装Flask...
pip install Flask==2.3.3

echo 2. 安装Flask-CORS...
pip install Flask-CORS==4.0.0

echo 3. 安装requests...
pip install requests==2.31.0

echo 4. 安装schedule...
pip install schedule==1.2.0

echo 5. 安装cryptography...
pip install cryptography==41.0.7

echo 6. 安装python-dotenv...
pip install python-dotenv==1.0.0

echo 7. 安装websocket-client...
pip install websocket-client==1.6.4

echo.
echo ✅ 核心依赖安装完成！
echo.
echo 📝 注意：跳过了numpy和pandas（需要C++编译器）
echo    系统核心功能不受影响，可以正常运行
echo.
echo 🚀 现在可以运行系统了：
echo   启动系统.bat
echo.
pause
