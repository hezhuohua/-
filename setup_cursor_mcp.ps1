# Cursor MCP Tools 配置工具
# 配置context7 MCP服务器到Cursor

Write-Host "🔧 Cursor MCP Tools 配置工具" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "📋 配置context7 MCP服务器到Cursor" -ForegroundColor Yellow
Write-Host ""

# 设置配置路径
$configPath = "$env:APPDATA\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings"
$configFile = "$configPath\cline_mcp_settings.json"

Write-Host "📁 准备配置目录..." -ForegroundColor Green
Write-Host "目标路径: $configFile" -ForegroundColor Gray

# 创建目录（如果不存在）
if (!(Test-Path $configPath)) {
    Write-Host "📁 创建配置目录..." -ForegroundColor Yellow
    try {
        New-Item -ItemType Directory -Path $configPath -Force | Out-Null
        Write-Host "✅ 配置目录创建成功" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ 无法创建配置目录: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "请检查权限或手动创建目录" -ForegroundColor Yellow
        Read-Host "按任意键退出"
        exit 1
    }
} else {
    Write-Host "✅ 配置目录已存在" -ForegroundColor Green
}

# MCP配置内容
$mcpConfig = @{
    mcpServers = @{
        context7 = @{
            url = "https://mcp.context7.com/mcp"
        }
    }
} | ConvertTo-Json -Depth 4

Write-Host "📝 写入MCP配置..." -ForegroundColor Green

try {
    # 写入配置文件
    $mcpConfig | Out-File -FilePath $configFile -Encoding UTF8
    Write-Host "✅ MCP配置文件创建成功！" -ForegroundColor Green
}
catch {
    Write-Host "❌ 配置文件写入失败: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

Write-Host ""
Write-Host "📋 配置文件内容:" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Gray
Get-Content $configFile | ForEach-Object { Write-Host $_ -ForegroundColor White }
Write-Host "----------------------------------------" -ForegroundColor Gray

Write-Host ""
Write-Host "🔍 验证配置..." -ForegroundColor Green

# 验证配置文件
if (Test-Path $configFile) {
    Write-Host "✅ 配置文件存在" -ForegroundColor Green
    $fileSize = (Get-Item $configFile).Length
    if ($fileSize -gt 0) {
        Write-Host "✅ 配置文件不为空 ($fileSize 字节)" -ForegroundColor Green
    } else {
        Write-Host "❌ 配置文件为空" -ForegroundColor Red
    }
} else {
    Write-Host "❌ 配置文件不存在" -ForegroundColor Red
}

Write-Host ""
Write-Host "🚀 后续步骤:" -ForegroundColor Cyan
Write-Host "1. 重启Cursor以使配置生效" -ForegroundColor White
Write-Host "2. 在Cursor中按 Ctrl+Shift+P 打开命令面板" -ForegroundColor White
Write-Host "3. 搜索 'MCP' 相关命令验证配置" -ForegroundColor White
Write-Host "4. 开始使用context7 MCP服务器功能！" -ForegroundColor White

Write-Host ""
Write-Host "💡 context7 MCP服务器功能:" -ForegroundColor Yellow
Write-Host "- 提供上下文感知的AI服务" -ForegroundColor White
Write-Host "- 智能代码分析和建议" -ForegroundColor White
Write-Host "- 基于上下文的代码生成" -ForegroundColor White
Write-Host "- 智能错误检测和修复" -ForegroundColor White

Write-Host ""
$restart = Read-Host "🔄 是否现在重启Cursor? (Y/N)"

if ($restart -eq "Y" -or $restart -eq "y") {
    Write-Host "🔄 正在重启Cursor..." -ForegroundColor Yellow
    try {
        # 关闭Cursor进程
        Get-Process -Name "Cursor" -ErrorAction SilentlyContinue | Stop-Process -Force
        Start-Sleep -Seconds 2

        # 启动Cursor
        Start-Process "cursor" -ArgumentList "`"$PWD`""
        Write-Host "✅ Cursor已重启" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️ 重启Cursor时遇到问题: $($_.Exception.Message)" -ForegroundColor Yellow
        Write-Host "请手动重启Cursor" -ForegroundColor White
    }
} else {
    Write-Host "💡 请手动重启Cursor以使配置生效" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Cursor MCP配置完成！" -ForegroundColor Green
Write-Host "📋 配置文件位置: $configFile" -ForegroundColor Gray

Read-Host "按任意键退出"
