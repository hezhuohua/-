@echo off
chcp 65001 >nul
echo 🚀 开始部署永续合约预测系统...
echo.

echo 📋 检查Git状态...
git status
echo.

echo 📦 添加文件到Git...
git add .
echo.

set /p commit_message="💬 请输入提交信息 (按Enter使用默认信息): "
if "%commit_message%"=="" (
    for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set mydate=%%c-%%a-%%b
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a:%%b
    set commit_message=更新永续合约预测系统 - !mydate! !mytime!
)

echo.
echo 💾 提交更改...
git commit -m "%commit_message%"
echo.

echo 🌐 推送到GitHub...
git push origin master
echo.

echo ✅ 部署完成！
echo 🔗 GitHub仓库: https://github.com/hezhuohua/-
echo 🌐 GitHub Pages: https://hezhuohua.github.io/-
echo ⏰ 请等待1-2分钟让GitHub Actions完成自动部署
echo.
echo 📊 您可以在以下链接查看部署状态:
echo https://github.com/hezhuohua/-/actions
echo.
pause
