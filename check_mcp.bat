@echo off
chcp 65001 >nul
echo 🔍 TestSprite MCP 配置检查工具
echo ================================

set "CONFIG_DIR=%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings"
set "CONFIG_FILE=%CONFIG_DIR%\cline_mcp_settings.json"

echo 📁 检查配置目录...
if exist "%CONFIG_DIR%" (
    echo ✅ 配置目录存在: %CONFIG_DIR%
) else (
    echo ❌ 配置目录不存在: %CONFIG_DIR%
    echo 💡 请运行 setup_mcp.bat 创建配置
    goto :end
)

echo.
echo 📄 检查配置文件...
if exist "%CONFIG_FILE%" (
    echo ✅ 配置文件存在: %CONFIG_FILE%
    
    for %%A in ("%CONFIG_FILE%") do (
        echo 📊 文件大小: %%~zA 字节
        echo 📅 修改时间: %%~tA
    )
    
    echo.
    echo 📋 配置文件内容:
    echo ----------------------------------------
    type "%CONFIG_FILE%"
    echo ----------------------------------------
    
) else (
    echo ❌ 配置文件不存在: %CONFIG_FILE%
    echo 💡 请运行 setup_mcp.bat 创建配置
    goto :end
)

echo.
echo 🔍 检查配置内容...
findstr /i "TestSprite" "%CONFIG_FILE%" >nul
if errorlevel 1 (
    echo ❌ 配置文件中未找到TestSprite配置
) else (
    echo ✅ 找到TestSprite配置
)

findstr /i "API_KEY" "%CONFIG_FILE%" >nul
if errorlevel 1 (
    echo ❌ 配置文件中未找到API_KEY
) else (
    echo ✅ 找到API_KEY配置
)

echo.
echo 🌐 检查网络环境...
echo 正在检查Node.js...
where node >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js未安装
    echo 💡 请从 https://nodejs.org 下载安装
) else (
    for /f "tokens=*" %%i in ('node --version 2^>nul') do echo ✅ Node.js版本: %%i
)

echo.
echo 正在检查npm...
where npm >nul 2>&1
if errorlevel 1 (
    echo ❌ npm未安装
) else (
    for /f "tokens=*" %%i in ('npm --version 2^>nul') do echo ✅ npm版本: %%i
)

echo.
echo 正在检查npx...
where npx >nul 2>&1
if errorlevel 1 (
    echo ❌ npx未安装
) else (
    echo ✅ npx可用
)

echo.
echo 🔍 检查VSCode...
where code >nul 2>&1
if errorlevel 1 (
    echo ❌ VSCode命令行工具不可用
    echo 💡 请在VSCode中安装Shell Command
) else (
    echo ✅ VSCode命令行工具可用
)

echo.
echo 📦 检查VSCode扩展目录...
set "VSCODE_EXT_DIR=%USERPROFILE%\.vscode\extensions"
if exist "%VSCODE_EXT_DIR%" (
    echo ✅ VSCode扩展目录存在
    
    echo 🔍 查找MCP相关扩展...
    dir /b "%VSCODE_EXT_DIR%" | findstr /i "cline\|mcp\|roo" >nul
    if errorlevel 1 (
        echo ⚠️ 未找到MCP相关扩展
        echo 💡 请确保已安装支持MCP的VSCode扩展
    ) else (
        echo ✅ 找到MCP相关扩展
        dir /b "%VSCODE_EXT_DIR%" | findstr /i "cline\|mcp\|roo"
    )
) else (
    echo ❌ VSCode扩展目录不存在
)

echo.
echo 🧪 测试MCP连接...
echo 正在测试TestSprite MCP包...
npx @testsprite/testsprite-mcp@latest --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 无法获取TestSprite MCP版本
    echo 💡 可能需要网络连接来下载包
) else (
    echo ✅ TestSprite MCP包可用
)

echo.
echo 📊 配置状态总结:
echo ================================
if exist "%CONFIG_FILE%" (
    echo ✅ MCP配置文件: 已创建
) else (
    echo ❌ MCP配置文件: 未创建
)

where node >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js环境: 未安装
) else (
    echo ✅ Node.js环境: 已安装
)

where code >nul 2>&1
if errorlevel 1 (
    echo ❌ VSCode CLI: 不可用
) else (
    echo ✅ VSCode CLI: 可用
)

echo.
echo 💡 建议操作:
if not exist "%CONFIG_FILE%" (
    echo 1. 运行 setup_mcp.bat 创建MCP配置
)
where node >nul 2>&1
if errorlevel 1 (
    echo 2. 安装Node.js环境
)
echo 3. 重启VSCode以使配置生效
echo 4. 在VSCode中测试MCP功能

:end
echo.
pause
