@echo off
echo ========================================
echo   移动端导航修复测试
echo ========================================
echo.

echo 正在启动代理服务器...
start /B python proxy_server.py

echo 等待服务器启动...
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo   测试页面已准备就绪！
echo ========================================
echo.
echo 本机测试地址:
echo   http://localhost:5000/mobile_fix_test.html
echo.
echo 移动设备测试地址:
echo   http://192.168.101.202:5000/mobile_fix_test.html
echo.
echo 主页面测试地址:
echo   http://192.168.101.202:5000/
echo.
echo ========================================
echo 按任意键打开测试页面...
pause > nul

start http://localhost:5000/mobile_fix_test.html

echo.
echo 测试说明:
echo 1. 在手机上访问测试页面
echo 2. 检查导航菜单显示是否正常
echo 3. 验证"模拟数据"红色警告框
echo 4. 测试触摸操作和响应
echo 5. 尝试横屏和竖屏切换
echo.

echo 按任意键退出...
pause > nul
