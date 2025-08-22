@echo off
chcp 65001 >nul
echo 🚀 永续合约预测系统 - 一键启动脚本
echo ========================================

echo 📦 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    echo 请安装Python 3.8+并添加到系统PATH
    pause
    exit /b 1
)

echo ✅ Python环境正常

echo 🚀 启动后端服务...
cd /d "C:\Users\Administrator\Desktop\永续合约预测系统开发\backend"
start "后端服务" /min python minimal_server.py

echo ⏳ 等待后端服务启动...
timeout /t 3 >nul

echo 🌐 启动前端服务...
cd /d "C:\Users\Administrator\Desktop\永续合约预测系统开发"
start "前端服务" /min python -m http.server 8080

echo ⏳ 等待前端服务启动...
timeout /t 3 >nul

echo 🖥️ 打开系统页面...
start "" "http://localhost:8080/index.html"

echo 📋 系统信息:
echo   - 前端界面: http://localhost:8080/index.html
echo   - 后端API: http://localhost:8000
echo   - API文档: http://localhost:8000/docs
echo   - 演示账号: demo@example.com / demo123

echo
echo ✅ 系统启动完成！请稍候浏览器自动打开...
echo ⚠️ 如浏览器未自动打开，请手动访问: http://localhost:8080/index.html
echo ⚠️ 按任意键关闭此窗口（服务将继续运行）

pause >nul