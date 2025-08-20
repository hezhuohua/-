# 开发环境配置指南

本文档详细说明如何配置永续合约预测系统的开发环境。

## 🛠️ VSCode 开发环境配置

### 1. 必需的扩展

系统已经为您配置了推荐的VSCode扩展，打开项目时VSCode会提示安装：

- **Python** - Python语言支持
- **Flake8** - Python代码检查
- **Black Formatter** - Python代码格式化
- **Vue Language Features (Volar)** - Vue.js支持
- **Tailwind CSS IntelliSense** - CSS框架支持
- **Live Server** - 本地开发服务器

### 2. MCP服务器配置（AI辅助开发）

为了获得更好的AI辅助开发体验，可以配置MCP服务器：

#### 配置步骤：

##### 方法一：VSCode命令面板配置（推荐）
1. **打开命令面板**：`Cmd/Ctrl + Shift + P`
2. **运行命令**：`MCP：添加服务器`
3. **选择安装类型**：`命令 (stdio)`
4. **输入命令**：`npx @testsprite/testsprite-mcp@latest`
5. **服务器标识符**：`TestSprite`
6. **选择配置范围**：根据需要选择
7. **添加环境变量**：设置API_KEY

##### 方法二：手动配置文件编辑
在VSCode的MCP配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "TestSprite": {
      "command": "npx",
      "args": ["@testsprite/testsprite-mcp@latest"],
      "env": {
        "API_KEY": "your-testsprite-api-key"
      }
    }
  }
}
```

##### 配置文件位置：
- **Windows**: `%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
- **macOS**: `~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`
- **Linux**: `~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/cline_mcp_settings.json`

#### API密钥获取：
1. 访问 [TestSprite官网](https://testsprite.com)
2. 注册账号并登录
3. 在控制台中生成API密钥
4. 将密钥添加到MCP配置中

#### MCP服务器功能：
- 🤖 **智能代码补全**：基于AI的代码建议和自动完成
- 🔍 **错误检测**：自动发现代码问题和修复建议
- 📝 **代码重构**：智能重构和优化建议
- 📚 **文档生成**：自动生成代码文档和注释
- 🧪 **测试生成**：自动生成单元测试代码
- 🔧 **代码解释**：解释复杂代码逻辑和功能
- 🚀 **性能优化**：代码性能分析和优化建议
- 🛡️ **安全检查**：代码安全漏洞检测

### 3. 调试配置

项目已配置了多个调试选项：

#### 可用的调试配置：
- **Python: FastAPI 后端服务** - 调试后端API
- **Python: 启动完整系统** - 调试整个系统
- **Python: 测试模块** - 调试测试用例

#### 使用方法：
1. 按 `F5` 或点击调试面板的运行按钮
2. 选择相应的调试配置
3. 设置断点进行调试

### 4. 任务配置

项目配置了常用的开发任务：

#### 可用任务：
- **安装Python依赖** - 安装requirements.txt中的依赖
- **启动后端服务** - 仅启动FastAPI后端
- **启动完整系统** - 启动前后端完整系统
- **运行代码格式化** - 使用Black格式化Python代码
- **运行代码检查** - 使用Flake8检查代码质量
- **运行测试** - 执行pytest测试
- **启动Live Server** - 启动前端开发服务器

#### 使用方法：
1. 按 `Cmd/Ctrl + Shift + P` 打开命令面板
2. 输入 `Tasks: Run Task`
3. 选择要执行的任务

## 🐍 Python 开发环境

### 1. 虚拟环境设置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 代码质量工具

#### Black (代码格式化)
```bash
# 格式化所有Python文件
black backend/ --line-length 88

# 检查格式但不修改
black backend/ --check
```

#### Flake8 (代码检查)
```bash
# 检查代码质量
flake8 backend/ --max-line-length=88 --extend-ignore=E203,W503
```

#### isort (导入排序)
```bash
# 排序导入语句
isort backend/
```

### 3. 测试环境

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_auth.py -v

# 生成测试覆盖率报告
pytest tests/ --cov=backend --cov-report=html
```

## 🌐 前端开发环境

### 1. 本地开发服务器

```bash
# 使用Python内置服务器
python -m http.server 8080

# 或使用Live Server扩展（推荐）
# 右键HTML文件 -> "Open with Live Server"
```

### 2. 前端调试

- 使用浏览器开发者工具
- Vue.js Devtools扩展
- 实时重载功能

## 🔧 环境变量配置

### 开发环境 (.env.development)
```env
DEBUG=True
DATABASE_URL=sqlite:///./crypto_prediction_dev.db
REDIS_URL=redis://localhost:6379/1
SECRET_KEY=dev-secret-key
DEEPSEEK_API_KEY=your-dev-api-key
```

### 生产环境 (.env.production)
```env
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/crypto_prediction
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-production-secret-key
DEEPSEEK_API_KEY=your-production-api-key
```

## 📊 数据库开发

### 1. 数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "描述"

# 执行迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### 2. 数据库工具

- **SQLite Browser** - 查看SQLite数据库
- **pgAdmin** - PostgreSQL管理工具
- **Redis Desktop Manager** - Redis可视化工具

## 🚀 部署准备

### 1. 生产环境检查清单

- [ ] 更新SECRET_KEY
- [ ] 配置生产数据库
- [ ] 设置环境变量
- [ ] 运行安全检查
- [ ] 执行性能测试
- [ ] 配置日志记录
- [ ] 设置监控告警

### 2. Docker部署

```bash
# 构建镜像
docker build -t crypto-prediction .

# 运行容器
docker run -p 8000:8000 crypto-prediction
```

## 🔍 故障排除

### 常见问题

1. **Python模块导入错误**
   - 检查PYTHONPATH设置
   - 确认虚拟环境激活

2. **数据库连接失败**
   - 检查数据库服务状态
   - 验证连接字符串

3. **前端资源加载失败**
   - 检查文件路径
   - 确认服务器运行状态

4. **API调用失败**
   - 检查网络连接
   - 验证API密钥

### 调试技巧

- 使用VSCode断点调试
- 查看浏览器控制台错误
- 检查服务器日志
- 使用Postman测试API

## 📚 开发资源

### 文档链接
- [FastAPI官方文档](https://fastapi.tiangolo.com/)
- [Vue.js官方文档](https://vuejs.org/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Redis文档](https://redis.io/documentation)

### 社区资源
- [GitHub Issues](https://github.com/your-repo/issues)
- [开发者论坛](https://forum.example.com)
- [技术博客](https://blog.example.com)

---

如有任何开发问题，请查看故障排除部分或联系开发团队。
