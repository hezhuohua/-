@echo off
chcp 65001 >nul
title 永续合约预测系统 - 移动端服务器

echo.
echo 🎯 永续合约预测系统 - 移动端服务器
echo ========================================
echo 让您的手机和其他设备都能访问系统
echo ========================================
echo.

echo 🚀 正在启动服务器...
python start_mobile_server.py

echo.
echo 👋 服务器已停止
pause
