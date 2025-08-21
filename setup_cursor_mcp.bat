@echo off
chcp 65001 >nul
echo 🔧 Cursor MCP Tools 配置工具
echo ================================
echo 📋 配置context7 MCP服务器到Cursor
echo.

echo 📁 准备配置目录...
set "CONFIG_DIR=%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings"
set "CONFIG_FILE=%CONFIG_DIR%\cline_mcp_settings.json"

echo 目标路径: %CONFIG_FILE%

if not exist "%CONFIG_DIR%" (
    echo 📁 创建配置目录...
    mkdir "%CONFIG_DIR%" 2>nul
    if errorlevel 1 (
        echo ❌ 无法创建配置目录
        echo 请检查权限或手动创建目录
        pause
        exit /b 1
    )
    echo ✅ 配置目录创建成功
) else (
    echo ✅ 配置目录已存在
)

echo 📝 写入MCP配置...
(
echo {
echo   "mcpServers": {
echo     "context7": {
echo       "url": "https://mcp.context7.com/mcp"
echo     }
echo   }
echo }
) > "%CONFIG_FILE%"

if errorlevel 1 (
    echo ❌ 配置文件写入失败
    pause
    exit /b 1
)

echo ✅ MCP配置文件创建成功！

echo.
echo 📋 配置文件内容:
echo ----------------------------------------
type "%CONFIG_FILE%"
echo ----------------------------------------

echo.
echo 🔍 验证配置...
if exist "%CONFIG_FILE%" (
    echo ✅ 配置文件存在
    for %%A in ("%CONFIG_FILE%") do (
        if %%~zA GTR 0 (
            echo ✅ 配置文件不为空 ^(%%~zA 字节^)
        ) else (
            echo ❌ 配置文件为空
        )
    )
) else (
    echo ❌ 配置文件不存在
)

echo.
echo 🚀 后续步骤:
echo 1. 重启Cursor以使配置生效
echo 2. 在Cursor中按 Ctrl+Shift+P 打开命令面板
echo 3. 搜索 "MCP" 相关命令验证配置
echo 4. 开始使用context7 MCP服务器功能！
echo.
echo 💡 context7 MCP服务器功能:
echo - 提供上下文感知的AI服务
echo - 智能代码分析和建议
echo - 基于上下文的代码生成
echo - 智能错误检测和修复
echo.
echo 🔄 是否现在重启Cursor? (Y/N)
set /p restart="请选择: "
if /i "%restart%"=="Y" (
    echo 🔄 正在重启Cursor...
    taskkill /f /im Cursor.exe >nul 2>&1
    timeout /t 2 >nul
    start "" cursor "%CD%"
    echo ✅ Cursor已重启
) else (
    echo 💡 请手动重启Cursor以使配置生效
)

echo.
echo ✅ Cursor MCP配置完成！
echo 📋 配置文件位置: %CONFIG_FILE%
pause
