# TestSprite MCP 配置指南

本文档详细说明如何在VSCode中配置TestSprite MCP服务器。

## 🔧 配置步骤

### 1. 找到MCP配置文件

根据您的操作系统，MCP配置文件位于：

**Windows:**
```
%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json
```

**macOS:**
```
~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
```

**Linux:**
```
~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
```

### 2. 配置内容

将以下配置添加到MCP配置文件中：

```json
{
  "mcpServers": {
    "TestSprite": {
      "command": "npx",
      "args": ["@testsprite/testsprite-mcp@latest"],
      "env": {
        "API_KEY": "your-testsprite-api-key-here"
      }
    }
  }
}
```

### 3. 您的实际配置

根据您之前提供的配置，您的MCP配置应该是：

```json
{
  "mcpServers": {
    "TestSprite": {
      "command": "npx",
      "args": ["@testsprite/testsprite-mcp@latest"],
      "env": {
        "API_KEY": "sk-user-DKSC0NlIoc3sBEvB5hzdm1bEhZIBmMiY6cch3oZwVMNe1VIehLlLT9nI7pRhGF0_zlEfdqDbTW5zfvqG_wweivXWHFs5TD2ZnLNTL2A9NEWMb-mK-U8cgl76JVHxDZAyH1w"
      }
    }
  }
}
```

## 🚀 快速配置脚本

### Windows PowerShell 脚本

创建 `setup_mcp.ps1` 文件：

```powershell
# 设置MCP配置
$configPath = "$env:APPDATA\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings"
$configFile = "$configPath\cline_mcp_settings.json"

# 创建目录（如果不存在）
if (!(Test-Path $configPath)) {
    New-Item -ItemType Directory -Path $configPath -Force
}

# MCP配置内容
$mcpConfig = @{
    mcpServers = @{
        TestSprite = @{
            command = "npx"
            args = @("@testsprite/testsprite-mcp@latest")
            env = @{
                API_KEY = "sk-user-DKSC0NlIoc3sBEvB5hzdm1bEhZIBmMiY6cch3oZwVMNe1VIehLlLT9nI7pRhGF0_zlEfdqDbTW5zfvqG_wweivXWHFs5TD2ZnLNTL2A9NEWMb-mK-U8cgl76JVHxDZAyH1w"
            }
        }
    }
} | ConvertTo-Json -Depth 4

# 写入配置文件
$mcpConfig | Out-File -FilePath $configFile -Encoding UTF8

Write-Host "✅ MCP配置已创建: $configFile"
Write-Host "🔄 请重启VSCode以使配置生效"
```

### 批处理脚本

创建 `setup_mcp.bat` 文件：

```batch
@echo off
chcp 65001 >nul
echo 🔧 配置TestSprite MCP服务器...

set "CONFIG_DIR=%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings"
set "CONFIG_FILE=%CONFIG_DIR%\cline_mcp_settings.json"

echo 📁 创建配置目录...
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"

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

echo ✅ MCP配置已创建: %CONFIG_FILE%
echo 🔄 请重启VSCode以使配置生效
echo.
echo 📋 配置文件内容:
type "%CONFIG_FILE%"
echo.
pause
```

## 🔍 验证配置

### 1. 检查配置文件是否存在

```bash
# Windows
dir "%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json"

# macOS/Linux
ls -la ~/Library/Application\ Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
```

### 2. 验证MCP服务器状态

在VSCode中：
1. 打开命令面板 (`Cmd/Ctrl + Shift + P`)
2. 搜索 "MCP" 相关命令
3. 检查TestSprite服务器是否正常运行

### 3. 测试AI功能

配置成功后，您应该能够：
- 获得智能代码补全
- 自动错误检测和修复建议
- 代码重构建议
- 自动文档生成

## 🛠️ 故障排除

### 常见问题

1. **配置文件不存在**
   - 手动创建目录和文件
   - 使用提供的脚本自动创建

2. **MCP服务器无法启动**
   - 检查Node.js是否已安装
   - 验证API密钥是否正确
   - 检查网络连接

3. **API密钥无效**
   - 确认API密钥格式正确
   - 检查API密钥是否过期
   - 重新生成API密钥

### 日志检查

查看VSCode的输出面板：
1. `View` → `Output`
2. 选择 "MCP" 或相关的输出通道
3. 查看错误信息和连接状态

## 📚 相关文档

- [TestSprite官方文档](https://testsprite.com/docs)
- [MCP协议规范](https://modelcontextprotocol.io/)
- [VSCode扩展开发指南](https://code.visualstudio.com/api)

## 🔄 更新配置

如果需要更新配置：
1. 修改配置文件
2. 重启VSCode
3. 验证新配置是否生效

---

**注意**: 请妥善保管您的API密钥，不要将其提交到版本控制系统中。
