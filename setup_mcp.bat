@echo off
chcp 65001 >nul
echo 🔧 TestSprite MCP 自动配置工具
echo ================================

echo 📋 检查VSCode安装...
where code >nul 2>&1
if errorlevel 1 (
    echo ⚠️ VSCode未安装或不在PATH中
    echo 请确保VSCode已正确安装
) else (
    echo ✅ VSCode已安装
)

echo 📁 准备配置目录...
set "CONFIG_DIR=%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings"
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
echo     "TestSprite": {
echo       "command": "npx",
echo       "args": ["@testsprite/testsprite-mcp@latest"],
echo       "env": {
echo         "API_KEY": "sk-user-DKSC0NlIoc3sBEvB5hzdm1bEhZIBmMiY6cch3oZwVMNe1VIehLlLT9nI7pRhGF0_zlEfdqDbTW5zfvqG_wweivXWHFs5TD2ZnLNTL2A9NEWMb-mK-U8cgl76JVHxDZAyH1w"
echo       }
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
echo 📦 检查Node.js环境...
where node >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Node.js未安装或不在PATH中
    echo TestSprite MCP需要Node.js环境
    echo 请从 https://nodejs.org 下载安装Node.js
) else (
    node --version
    echo ✅ Node.js环境正常
)

echo.
echo 📦 检查npm环境...
where npm >nul 2>&1
if errorlevel 1 (
    echo ⚠️ npm未安装
) else (
    npm --version
    echo ✅ npm环境正常
)

echo.
echo 🚀 后续步骤:
echo 1. 重启VSCode以使配置生效
echo 2. 在VSCode中按 Ctrl+Shift+P 打开命令面板
echo 3. 搜索 "MCP" 相关命令验证配置
echo 4. 开始享受AI辅助编程功能！
echo.
echo 💡 功能特性:
echo - 智能代码补全和建议
echo - 自动错误检测和修复
echo - 代码重构和优化建议
echo - 自动文档和注释生成
echo - 单元测试代码生成
echo - 代码解释和分析
echo.
echo 📚 更多信息请查看: MCP_CONFIG_GUIDE.md
echo.

echo 🔄 是否现在重启VSCode? (Y/N)
set /p restart="请选择: "
if /i "%restart%"=="Y" (
    echo 🔄 正在重启VSCode...
    taskkill /f /im Code.exe >nul 2>&1
    timeout /t 2 >nul
    start "" code "%CD%"
    echo ✅ VSCode已重启
) else (
    echo 💡 请手动重启VSCode以使配置生效
)

echo.
echo ✅ MCP配置完成！
pause
