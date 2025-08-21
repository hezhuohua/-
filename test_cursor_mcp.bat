@echo off
chcp 65001 >nul
echo 🔍 Cursor MCP配置测试工具
echo ================================
echo.

echo 📋 检查配置文件...
set "CONFIG_DIR=%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings"
set "CONFIG_FILE=%CONFIG_DIR%\cline_mcp_settings.json"

echo 配置目录: %CONFIG_DIR%
echo 配置文件: %CONFIG_FILE%
echo.

if exist "%CONFIG_FILE%" (
    echo ✅ 配置文件存在
    echo.
    echo 📋 配置文件内容:
    echo ----------------------------------------
    type "%CONFIG_FILE%"
    echo ----------------------------------------
    echo.

    for %%A in ("%CONFIG_FILE%") do (
        if %%~zA GTR 0 (
            echo ✅ 配置文件大小: %%~zA 字节
        ) else (
            echo ❌ 配置文件为空
        )
    )

    echo.
    echo 🔍 验证JSON格式...
    powershell -Command "try { $config = Get-Content '%CONFIG_FILE%' | ConvertFrom-Json; Write-Host '✅ JSON格式正确' -ForegroundColor Green; Write-Host 'MCP服务器数量:' $config.mcpServers.PSObject.Properties.Count } catch { Write-Host '❌ JSON格式错误:' $_.Exception.Message -ForegroundColor Red }"

) else (
    echo ❌ 配置文件不存在
    echo.
    echo 💡 请先运行 setup_cursor_mcp.bat 创建配置
)

echo.
echo 🔍 检查Cursor进程...
tasklist /fi "imagename eq Cursor.exe" 2>nul | find "Cursor.exe" >nul
if errorlevel 1 (
    echo ⚠️ Cursor未运行
    echo 💡 请启动Cursor以测试MCP功能
) else (
    echo ✅ Cursor正在运行
    echo 💡 可以在Cursor中按 Ctrl+Shift+P 搜索MCP命令进行测试
)

echo.
echo 🔍 检查网络连接...
ping -n 1 mcp.context7.com >nul 2>&1
if errorlevel 1 (
    echo ❌ 无法连接到 mcp.context7.com
    echo 💡 请检查网络连接
) else (
    echo ✅ 网络连接正常
)

echo.
echo 📚 测试建议:
echo 1. 确保配置文件存在且格式正确
echo 2. 重启Cursor以使配置生效
echo 3. 在Cursor中按 Ctrl+Shift+P 打开命令面板
echo 4. 搜索 "MCP" 相关命令
echo 5. 检查context7服务器状态
echo.
echo 💡 如果遇到问题，请查看 CURSOR_MCP_SETUP.md 获取详细帮助

echo.
pause
