@echo off
chcp 65001 >nul
echo ========================================
echo 📊 实时数据状态检查
echo ========================================
echo.

echo 🔍 检查WebSocket服务器 (端口8000)...
netstat -an | findstr :8000 >nul
if %errorlevel% equ 0 (
    echo ✅ WebSocket服务器正在运行
    netstat -an | findstr :8000
) else (
    echo ❌ WebSocket服务器未运行
)

echo.
echo 🔍 检查HTTP服务器 (端口8080)...
netstat -an | findstr :8080 >nul
if %errorlevel% equ 0 (
    echo ✅ HTTP服务器正在运行
    netstat -an | findstr :8080
) else (
    echo ❌ HTTP服务器未运行
)

echo.
echo 📡 测试WebSocket连接...
curl -s http://localhost:8000/health >nul
if %errorlevel% equ 0 (
    echo ✅ WebSocket服务健康检查通过
) else (
    echo ❌ WebSocket服务健康检查失败
)

echo.
echo 🌐 测试HTTP服务...
curl -s http://localhost:8080 >nul
if %errorlevel% equ 0 (
    echo ✅ HTTP服务正常
) else (
    echo ❌ HTTP服务异常
)

echo.
echo ========================================
echo 📋 服务状态总结：
echo.
if exist "websocket_test.html" (
    echo ✅ WebSocket测试页面已创建
    echo   访问: http://localhost:8080/websocket_test.html
) else (
    echo ❌ WebSocket测试页面未找到
)

echo.
echo 🎯 实时数据状态：
echo   主页面: http://localhost:8080
echo   WebSocket: ws://localhost:8000/ws
echo.
echo 💡 如果看到绿色状态指示器，说明实时数据已启用
echo ========================================
pause
