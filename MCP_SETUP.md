# MCP服务器配置指南

本指南将帮助您在VSCode中配置TestSprite MCP服务器，以获得强大的AI辅助开发功能。

## 🤖 什么是MCP？

MCP (Model Context Protocol) 是一个标准协议，允许AI模型与开发工具进行深度集成，提供智能代码辅助功能。

## 🚀 快速配置

### 方法一：VSCode命令面板配置（推荐）

1. **打开VSCode**并加载项目
2. **打开命令面板**：`Cmd/Ctrl + Shift + P`
3. **输入并选择**：`MCP：添加服务器`
4. **选择安装类型**：`命令 (stdio)`
5. **输入命令**：`npx @testsprite/testsprite-mcp@latest`
6. **设置标识符**：`TestSprite`
7. **选择配置范围**：选择适合的范围（用户或工作区）
8. **添加环境变量**：
   - 变量名：`API_KEY`
   - 变量值：您的TestSprite API密钥

### 方法二：手动配置文件编辑

1. **找到MCP配置文件位置**：
   - **Windows**: `%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
   - **macOS**: `~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
   - **Linux**: `~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`

2. **编辑配置文件**，添加以下内容：

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

3. **替换API密钥**：将 `your-testsprite-api-key-here` 替换为您的实际API密钥

4. **保存文件**并重启VSCode

## 🔑 获取API密钥

### TestSprite API密钥获取步骤：

1. **访问官网**：[https://testsprite.com](https://testsprite.com)
2. **注册账号**：创建新账号或使用现有账号登录
3. **进入控制台**：登录后进入用户控制台
4. **生成API密钥**：
   - 找到API密钥管理页面
   - 点击"生成新密钥"
   - 复制生成的密钥
5. **保存密钥**：将密钥安全保存，用于MCP配置

### API密钥安全提示：
- ⚠️ **不要将API密钥提交到版本控制系统**
- 🔒 **定期轮换API密钥**
- 👥 **不要与他人分享API密钥**
- 📝 **为不同项目使用不同的API密钥**

## ✨ MCP功能特性

配置完成后，您将获得以下AI辅助功能：

### 🤖 智能代码补全
- 基于上下文的代码建议
- 自动完成函数和变量名
- 智能导入语句建议

### 🔍 错误检测与修复
- 实时代码错误检测
- 自动修复建议
- 代码质量改进提示

### 📝 代码重构
- 智能重构建议
- 代码优化提示
- 性能改进建议

### 📚 文档生成
- 自动生成函数文档
- 代码注释建议
- API文档生成

### 🧪 测试生成
- 自动生成单元测试
- 测试用例建议
- 测试覆盖率分析

### 🔧 代码解释
- 复杂代码逻辑解释
- 算法原理说明
- 最佳实践建议

## 🛠️ 故障排除

### 常见问题及解决方案：

#### 1. MCP服务器无法启动
**问题**：VSCode显示MCP服务器连接失败
**解决方案**：
- 检查网络连接
- 验证API密钥是否正确
- 重启VSCode
- 检查Node.js是否已安装

#### 2. API密钥无效
**问题**：提示API密钥无效或过期
**解决方案**：
- 重新生成API密钥
- 检查密钥是否完整复制
- 确认账号状态正常

#### 3. 功能不可用
**问题**：MCP功能无法使用
**解决方案**：
- 检查VSCode扩展是否最新
- 重新安装MCP相关扩展
- 清除VSCode缓存

#### 4. 性能问题
**问题**：MCP响应缓慢
**解决方案**：
- 检查网络延迟
- 减少同时处理的请求
- 升级网络带宽

## 📊 使用统计

配置完成后，您可以在VSCode中查看MCP使用统计：
- 代码补全使用次数
- 错误修复建议数量
- 文档生成统计
- 性能改进建议

## 🔄 更新与维护

### 定期维护任务：
1. **更新MCP服务器**：`npx @testsprite/testsprite-mcp@latest`
2. **检查API配额**：监控API使用量
3. **更新配置**：根据新功能调整配置
4. **备份设置**：定期备份MCP配置

### 版本更新：
- 关注TestSprite官方更新
- 查看新功能发布说明
- 测试新版本兼容性

## 📞 技术支持

如果遇到配置问题，可以通过以下方式获取帮助：

- 📧 **邮箱支持**：support@testsprite.com
- 📖 **官方文档**：[https://docs.testsprite.com](https://docs.testsprite.com)
- 💬 **社区论坛**：[https://community.testsprite.com](https://community.testsprite.com)
- 🐛 **问题反馈**：[https://github.com/testsprite/issues](https://github.com/testsprite/issues)

## 🎯 最佳实践

1. **合理使用API配额**：避免过度调用API
2. **定期清理缓存**：保持系统性能
3. **及时更新**：使用最新版本获得最佳体验
4. **安全配置**：保护API密钥安全
5. **反馈问题**：及时报告bug和建议

---

配置完成后，您将拥有强大的AI辅助开发能力，大大提升编程效率和代码质量！
