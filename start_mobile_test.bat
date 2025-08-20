@echo off
echo ========================================
echo   永续合约预测系统 - 移动端测试
echo ========================================
echo.

echo 正在启动代理服务器...
start /B python proxy_server.py

echo 等待服务器启动...
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo   服务器已启动！
echo ========================================
echo.
echo 本机访问地址:
echo   http://localhost:5000
echo.
echo 移动设备访问地址:
echo   http://192.168.101.202:5000
echo.
echo 测试页面:
echo   http://192.168.101.202:5000/mobile_test.html
echo.
echo ========================================
echo 按任意键打开浏览器...
pause > nul

start http://localhost:5000

echo.
echo 提示:
echo 1. 在手机上访问 http://192.168.101.202:5000
echo 2. 使用浏览器开发者工具模拟移动设备
echo 3. 按 Ctrl+C 停止服务器
echo.

pause
