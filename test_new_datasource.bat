@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🚀 币安API数据源测试
echo ========================================
echo.

echo 📊 步骤1: 测试币安API连接...
python test_binance_api.py

echo.
echo ========================================
echo 📊 步骤2: 启动后端服务器...
echo ========================================
echo.

echo 正在启动后端服务器...
start /B python server.py

echo 等待服务器启动...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo 📊 步骤3: 测试后端API...
echo ========================================
echo.

echo 测试后端市场数据API...
curl -s http://localhost:5000/api/market-data | python -m json.tool

echo.
echo ========================================
echo 📊 步骤4: 打开前端页面...
echo ========================================
echo.

echo 正在打开前端页面...
start index.html

echo.
echo ✅ 测试完成！
echo.
echo 📋 测试结果说明：
echo - 如果看到BTC价格数据，说明币安API连接正常
echo - 如果后端API返回数据，说明后端服务正常
echo - 如果前端页面显示实时价格，说明数据源配置成功
echo.
echo 🔧 如果遇到问题：
echo 1. 检查网络连接
echo 2. 确保Python和requests库已安装
echo 3. 检查防火墙设置
echo.
pause
