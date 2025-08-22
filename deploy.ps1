# 永续合约预测系统 - PowerShell部署脚本
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 永续合约预测系统 - 自动部署脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查Git状态
Write-Host "📋 检查Git状态..." -ForegroundColor Yellow
git status
Write-Host ""

# 拉取最新代码
Write-Host "🔄 拉取最新代码..." -ForegroundColor Yellow
git pull origin master
Write-Host ""

# 检查依赖
Write-Host "📦 检查依赖..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "📥 安装Node.js依赖..." -ForegroundColor Green
    npm install
}
else {
    Write-Host "✅ 依赖已存在" -ForegroundColor Green
}
Write-Host ""

# 启动服务器
Write-Host "🌐 启动开发服务器..." -ForegroundColor Yellow
Write-Host "服务器将在以下地址启动：" -ForegroundColor White
Write-Host "- 本地访问: http://127.0.0.1:8088" -ForegroundColor Green
Write-Host "- 局域网访问: http://192.168.101.202:8088" -ForegroundColor Green
Write-Host "- 外部访问: http://198.18.0.1:8088" -ForegroundColor Green
Write-Host ""
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Red
Write-Host ""

# 启动HTTP服务器
npx http-server -p 8088 -o
