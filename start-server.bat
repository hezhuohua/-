@echo off
echo 正在启动永续合约预测系统服务器...
echo 服务器地址: http://localhost:8088
echo 按 Ctrl+C 停止服务器
echo.
npx http-server -p 8088 -o
pause
