@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 永续合约预测系统 - 自动部署脚本
echo ========================================
echo.

echo 📋 检查Git状态...
git status
echo.

echo 🔄 拉取最新代码...
git pull origin master
echo.

echo 📦 检查依赖...
if not exist "node_modules" (
    echo 📥 安装Node.js依赖...
    npm install
) else (
    echo ✅ 依赖已存在
)
echo.

echo 🌐 启动开发服务器...
echo 服务器将在以下地址启动：
echo - 本地访问: http://127.0.0.1:8088
echo - 局域网访问: http://192.168.101.202:8088
echo - 外部访问: http://198.18.0.1:8088
echo.
echo 按 Ctrl+C 停止服务器
echo.

npx http-server -p 8088 -o
