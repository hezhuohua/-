@echo off
chcp 65001 >nul
title 永续合约预测系统

echo.
echo ========================================
echo   永续合约预测系统启动脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

echo 正在安装依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo ✅ 依赖安装完成
echo.

echo 正在启动系统...
python run.py

pause
