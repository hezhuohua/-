# Cursor MCP Tools 配置指南

本文档详细说明如何将context7 MCP服务器配置到Cursor的MCP Tools中。

## 🎯 配置目标

将以下MCP服务器配置添加到Cursor：

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

## 🔧 自动配置方法

### 方法1：使用批处理脚本（推荐Windows用户）

1. 双击运行 `setup_cursor_mcp.bat`
2. 脚本会自动创建配置目录和文件
3. 选择是否自动重启Cursor

### 方法2：使用PowerShell脚本（推荐高级用户）

1. 右键点击 `setup_cursor_mcp.ps1`
2. 选择"使用PowerShell运行"
3. 按照提示完成配置

### 方法3：手动配置

#### 步骤1：找到Cursor配置目录

**Windows:**
```
%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\
```

**macOS:**
```
~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/
```

**Linux:**
```
~/.config/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/
```

#### 步骤2：创建配置文件

在配置目录中创建 `cline_mcp_settings.json` 文件，内容如下：

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

## 📁 配置文件结构

```
%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\
└── cline_mcp_settings.json
```

## ✅ 验证配置

### 1. 检查配置文件

确认 `cline_mcp_settings.json` 文件存在且内容正确：

```bash
# Windows
dir "%APPDATA%\Cursor\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json"

# macOS/Linux
ls -la ~/Library/Application\ Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json
```

### 2. 重启Cursor

配置完成后必须重启Cursor以使配置生效。

### 3. 验证MCP服务器状态

在Cursor中：
1. 按 `Ctrl+Shift+P` 打开命令面板
2. 搜索 "MCP" 相关命令
3. 检查context7服务器是否正常运行

## 🚀 context7 MCP服务器功能

配置成功后，您将获得以下功能：

- **上下文感知AI服务**：基于当前代码上下文的智能建议
- **智能代码分析**：自动分析代码结构和潜在问题
- **代码生成**：根据上下文自动生成相关代码
- **错误检测**：智能识别和修复代码错误
- **代码优化**：提供代码重构和性能优化建议

## 🛠️ 故障排除

### 常见问题

1. **配置文件不存在**
   - 检查配置目录路径是否正确
   - 确认有足够的权限创建文件和目录
   - 使用提供的脚本自动创建

2. **MCP服务器无法连接**
   - 检查网络连接是否正常
   - 验证URL地址是否正确
   - 确认context7服务是否可用

3. **配置不生效**
   - 确保已重启Cursor
   - 检查配置文件格式是否正确
   - 查看Cursor的错误日志

### 日志检查

查看Cursor的输出面板：
1. `View` → `Output`
2. 选择相关的输出通道
3. 查看错误信息和连接状态

## 📚 相关资源

- [MCP协议规范](https://modelcontextprotocol.io/)
- [Cursor官方文档](https://cursor.sh/docs)
- [context7 MCP服务器](https://mcp.context7.com)

## 🔄 更新配置

如果需要修改配置：
1. 编辑 `cline_mcp_settings.json` 文件
2. 重启Cursor
3. 验证新配置是否生效

## ⚠️ 注意事项

1. **权限要求**：确保有足够的权限访问配置目录
2. **网络连接**：context7 MCP服务器需要网络连接
3. **服务可用性**：确保context7服务正常运行
4. **配置备份**：建议备份原始配置文件

## 🎉 配置完成

配置成功后，您就可以在Cursor中使用context7 MCP服务器的强大功能了！

---

**快速开始**：运行 `setup_cursor_mcp.bat` 或 `setup_cursor_mcp.ps1` 即可自动完成配置。
