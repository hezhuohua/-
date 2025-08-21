@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 永续合约预测系统 - 实时数据启动器
echo ========================================
echo.

echo 📡 正在启动WebSocket服务器...
start "WebSocket Server" cmd /k "cd backend && py minimal_server.py"

echo ⏳ 等待WebSocket服务器启动...
timeout /t 3 /nobreak >nul

echo 🌐 正在启动HTTP服务器...
start "HTTP Server" cmd /k "py -m http.server 8080"

echo.
echo ✅ 服务启动完成！
echo.
echo 📍 访问地址：
echo    - 主页面: http://localhost:8080
echo    - WebSocket测试: http://localhost:8080/websocket_test.html
echo    - WebSocket服务: ws://localhost:8000/ws
echo.
echo 💡 提示：
echo    - 实时数据状态会在主页面顶部显示
echo    - 绿色状态表示实时数据已连接
echo    - 黄色状态表示使用模拟数据
echo.
echo 🔄 按任意键退出...
pause >nul
