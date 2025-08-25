@echo off
chcp 65001 >nul
title Conda依赖安装器

echo.
echo ========================================
echo   🐍 Conda依赖安装器
echo ========================================
echo.

:: 检查conda是否可用
conda --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到conda，请先安装Anaconda或Miniconda
    echo 下载地址: https://www.anaconda.com/download
    pause
    exit /b 1
)

echo ✅ 检测到conda环境
echo.

echo 📦 正在使用conda安装依赖...
echo.

:: 使用conda安装依赖
conda install -c conda-forge flask=2.3.3 flask-cors=4.0.0 requests=2.31.0 schedule=1.2.0 cryptography=41.0.7 python-dotenv=1.0.0 websocket-client=1.6.4 numpy=1.26.4 pandas=2.1.4 -y

if errorlevel 1 (
    echo ❌ conda安装失败，尝试使用pip...
    goto pip_fallback
)

echo.
echo ✅ 所有依赖安装完成！
echo.
echo 🚀 现在可以运行系统了：
echo   启动系统.bat
echo.
pause
exit /b 0

:pip_fallback
echo.
echo 🔄 切换到pip安装方式...
call install_deps_simple.bat
