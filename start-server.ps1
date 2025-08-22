Write-Host "正在启动永续合约预测系统服务器..." -ForegroundColor Green
Write-Host "服务器地址: http://localhost:8088" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Yellow
Write-Host ""

try {
    npx http-server -p 8088 -o
}
catch {
    Write-Host "启动失败，请检查Node.js是否正确安装" -ForegroundColor Red
    Read-Host "按任意键退出"
}
