# 🚀 永续合约预测系统

基于AI大模型的专业级加密货币永续合约预测平台，集成多交易所实时数据，提供智能预测和专业交易工具。

## 🌐 在线演示

- **GitHub Pages**: [https://hezhuohua.github.io/-](https://hezhuohua.github.io/-)
- **GitHub仓库**: [https://github.com/hezhuohua/-](https://github.com/hezhuohua/-)

## 📋 自动部署状态

![部署状态](https://github.com/hezhuohua/-/workflows/部署永续合约预测系统到GitHub%20Pages/badge.svg)

## 🌟 核心功能

### 📊 实时交易仪表盘
- **多交易所数据同步**: 集成Binance、OKX、Bybit等10大交易所
- **专业级图表**: TradingView图表集成，支持多种技术指标
- **实时价格监控**: 毫秒级数据更新，价格差异分析
- **深度图展示**: 买卖盘深度可视化
- **套利机会识别**: 自动发现跨交易所价格差异

### 🤖 AI智能预测
- **DEEPSEEK大模型**: 集成最新AI技术进行市场分析
- **多时间粒度**: 支持1分钟到1小时的预测时间框架
- **综合分析**: 技术面+基本面+情绪面多维度分析
- **预测准确率**: 实时统计和历史回测
- **智能推荐**: 基于用户偏好的个性化建议

### 💎 会员服务体系
- **灵活收费模式**: 试用版+分级会员+按次付费
- **多种支付方式**: 支持支付宝、微信等多种支付
- **收款码管理**: 后台可随时更换收款二维码
- **人工审核**: 支付凭证人工确认机制
- **会员特权**: 不同等级享受不同功能权限

## 🚀 快速开始

### 方式一：在线演示（推荐）
直接打开 `demo.html` 文件即可体验系统功能：

```bash
# 下载项目
git clone <repository-url>
cd 永续合约预测系统开发

# 直接在浏览器中打开演示页面
open demo.html
```

### 方式二：完整部署
运行完整的前后端系统：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行启动脚本
python run_server.py
```

### 方式三：开发环境快速设置
使用自动化脚本设置完整的开发环境：

```bash
# 运行开发环境设置脚本
python setup_dev.py

# 激活虚拟环境（根据提示）
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 重新运行设置脚本完成安装
python setup_dev.py
```

访问地址：
- 前端界面: http://localhost:8080
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 📁 项目结构

```
永续合约预测系统开发/
├── backend/                 # 后端代码
│   ├── main.py             # FastAPI主应用
│   ├── models.py           # 数据库模型
│   ├── auth.py             # 用户认证
│   ├── exchange_manager.py # 交易所数据管理
│   ├── prediction_service.py # AI预测服务
│   └── payment_service.py  # 支付服务
├── .vscode/                # VSCode配置
│   ├── settings.json       # 工作区设置
│   ├── launch.json         # 调试配置
│   ├── tasks.json          # 任务配置
│   ├── extensions.json     # 推荐扩展
│   └── mcp_config_example.json # MCP配置示例
├── tests/                  # 测试文件
│   ├── __init__.py         # 测试模块初始化
│   └── test_basic.py       # 基础功能测试
├── index.html              # 完整前端界面
├── demo.html               # 演示页面（可直接运行）
├── run_server.py           # 启动脚本
├── setup_dev.py            # 开发环境设置脚本
├── requirements.txt        # Python依赖
├── README.md              # 项目说明
├── DEVELOPMENT.md         # 开发指南
└── MCP_SETUP.md           # MCP配置指南
```

## 🎯 功能演示

### 1. 实时交易仪表盘
![交易仪表盘](https://via.placeholder.com/800x400?text=Trading+Dashboard)

- 多交易所价格实时对比
- 专业K线图表展示
- 深度图和订单簿
- 套利机会提醒

### 2. AI智能预测
![AI预测](https://via.placeholder.com/800x400?text=AI+Prediction)

- 多时间框架预测
- 预测置信度显示
- 详细分析说明
- 历史准确率统计

### 3. 会员中心
![会员中心](https://via.placeholder.com/800x400?text=Membership+Center)

- 用户配额管理
- 套餐选择升级
- 使用统计分析
- 支付记录查询

## 💰 收费模式

| 套餐类型 | 价格 | 每日预测次数 | 特色功能 |
|---------|------|-------------|----------|
| 试用版 | 免费 | 50次 | 24小时体验 |
| 基础版 | ¥99/月 | 200次 | 基础技术指标 |
| 专业版 | ¥299/月 | 500次 | 高级分析+优先客服 |
| 旗舰版 | ¥599/月 | 无限次 | 全功能+API接口 |

## 🔧 技术架构

### 后端技术栈
- **FastAPI**: 高性能异步Web框架
- **SQLAlchemy**: ORM数据库操作
- **Redis**: 实时数据缓存
- **WebSocket**: 实时数据推送
- **DEEPSEEK API**: AI大模型集成

### 前端技术栈
- **Vue.js 3**: 现代化前端框架
- **TradingView**: 专业图表库
- **WebSocket**: 实时数据接收
- **响应式设计**: 支持移动端

### 数据源
- **Binance API**: 全球最大交易所
- **OKX API**: 衍生品专业平台
- **Bybit API**: 永续合约专家
- **其他7大交易所**: 全面数据覆盖

## 🛠️ 配置说明

### 环境变量配置
创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=sqlite:///./crypto_prediction.db

# Redis配置
REDIS_URL=redis://localhost:6379

# JWT密钥
SECRET_KEY=your-secret-key-change-in-production

# DEEPSEEK API配置
DEEPSEEK_API_KEY=your-deepseek-api-key

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 数据库初始化
系统会自动创建SQLite数据库和必要的表结构。

### Redis配置（可选）
Redis用于实时数据缓存，如果没有安装Redis，系统会使用内存缓存。

### VSCode开发环境配置

#### MCP服务器配置（用于AI辅助开发）
如果您使用VSCode进行开发，可以配置MCP服务器来获得更好的AI辅助：

##### 自动配置方式：
1. **打开命令面板**：`Cmd/Ctrl + Shift + P`
2. **运行命令**：`MCP：添加服务器`
3. **选择安装类型**：`命令 (stdio)`
4. **输入命令**：`npx @testsprite/testsprite-mcp@latest`
5. **服务器标识符**：`TestSprite`
6. **选择配置范围**：根据需要选择
7. **添加配置**：`env`
8. **设置API密钥**：在环境变量中配置您的API密钥

##### 手动配置方式：
如果需要手动配置，可以在VSCode的MCP配置文件中添加：

```json
{
  "mcpServers": {
    "TestSprite": {
      "command": "npx",
      "args": ["@testsprite/testsprite-mcp@latest"],
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

##### MCP服务器功能：
- 🤖 **智能代码补全**：基于AI的代码建议和自动完成
- 🔍 **错误检测**：自动发现代码问题和修复建议
- 📝 **代码重构**：智能重构和优化建议
- 📚 **文档生成**：自动生成代码文档和注释
- 🧪 **测试生成**：自动生成单元测试代码
- 🔧 **代码解释**：解释复杂代码逻辑和功能

#### 推荐的VSCode扩展
创建 `.vscode/extensions.json`：

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "bradlc.vscode-tailwindcss",
    "vue.volar",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-vscode-remote.remote-containers",
    "ms-toolsai.jupyter"
  ]
}
```

#### 工作区设置
创建 `.vscode/settings.json`：

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "files.associations": {
    "*.html": "html"
  },
  "emmet.includeLanguages": {
    "vue-html": "html"
  },
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### 调试配置
创建 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/main.py",
      "console": "integratedTerminal",
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },
    {
      "name": "Python: 启动脚本",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/run_server.py",
      "console": "integratedTerminal"
    }
  ]
}
```

## 📱 移动端支持

系统采用响应式设计，完美支持：
- 📱 手机浏览器
- 📱 平板设备
- 💻 桌面浏览器
- 🖥️ 大屏显示器

## 🔒 安全特性

- **JWT认证**: 安全的用户身份验证
- **密码加密**: bcrypt密码哈希
- **支付安全**: 不存储敏感支付信息
- **数据加密**: 用户数据加密存储
- **API限流**: 防止恶意请求

## 📈 性能优化

- **异步处理**: 高并发数据处理
- **数据压缩**: 优化传输性能
- **缓存策略**: 多级缓存机制
- **连接池**: 数据库连接优化
- **CDN加速**: 静态资源优化

## 🎮 使用指南

### 1. 开发环境配置
- 运行 `python setup_dev.py` 快速设置开发环境
- 查看 [DEVELOPMENT.md](DEVELOPMENT.md) 了解详细配置
- 配置MCP服务器获得AI辅助：[MCP_SETUP.md](MCP_SETUP.md)

### 2. 注册登录
- 点击右上角"登录"按钮
- 选择注册新账号或使用演示账号
- 演示账号：demo@example.com / demo123

### 3. 查看实时行情
- 在交易仪表盘查看多交易所价格
- 切换不同交易对（BTC/USDT, ETH/USDT）
- 选择参照交易所进行价格对比
- 观察价格差异和套利机会

### 4. 进行AI预测
- 切换到"AI预测"页面
- 选择交易对和参照交易所
- 选择预测时间框架
- 点击"开始预测"获取AI分析结果

### 5. 管理会员
- 查看当前配额和会员等级
- 选择合适的升级套餐
- 完成支付激活会员

## 🔍 代码质量分析

### 代码问题检查
项目已通过TestSprite MCP进行全面的代码质量分析，发现的问题和修复方案请查看：

- 📊 [CODE_ISSUES_REPORT.md](./CODE_ISSUES_REPORT.md) - 完整的问题分析报告
- 🔒 [SECURITY_FIXES.md](./SECURITY_FIXES.md) - 安全问题修复指南
- 🚀 [PERFORMANCE_FIXES.md](./PERFORMANCE_FIXES.md) - 性能优化指南
- 🧪 [TEST_IMPROVEMENTS.md](./TEST_IMPROVEMENTS.md) - 测试改进指南

### 快速修复
运行自动化修复脚本：

```bash
# 运行快速修复（会自动备份原文件）
python quick_fixes.py

# 安装新增的依赖
pip install -r requirements.txt

# 运行测试验证修复
pytest
```

### AI辅助修复
您可以将任何修复指南文档提供给AI助手，请求具体的代码修复：

```
请根据 SECURITY_FIXES.md 文档中的指导，帮我修复 backend/auth.py 文件中的安全问题。
```

## 🤝 技术支持

如需完整源码、部署支持或定制开发，请联系：

- 📧 邮箱：support@example.com
- 💬 微信：crypto_support
- 🔗 官网：https://example.com

## 🚀 自动部署

本项目已配置GitHub Actions自动部署到GitHub Pages。

### 部署流程

1. **自动部署**：推送代码到master分支会自动触发部署
2. **手动部署**：使用提供的脚本快速部署

#### Windows用户
```bash
# 双击运行或在命令行执行
deploy.bat
```

#### Linux/Mac用户
```bash
# 给脚本执行权限
chmod +x deploy.sh
# 运行部署脚本
./deploy.sh
```

#### 手动Git命令
```bash
git add .
git commit -m "更新描述"
git push origin master
```

### 部署状态查看

- **GitHub Actions**: [查看部署状态](https://github.com/hezhuohua/-/actions)
- **部署日志**: 在Actions页面查看详细部署日志
- **访问网站**: [https://hezhuohua.github.io/-](https://hezhuohua.github.io/-)

### 部署配置

部署配置文件位于：`.github/workflows/deploy.yml`

主要特性：
- ✅ 自动检测代码变更
- ✅ 自动构建和部署
- ✅ 支持自定义域名
- ✅ 404页面自动重定向
- ✅ 部署信息记录

## 📄 许可证

本项目仅供学习和演示使用，商业使用请联系获取授权。

## 🙏 致谢

感谢以下开源项目和服务：
- Vue.js 团队
- FastAPI 团队
- TradingView 图表库
- GitHub Pages 免费托管
- GitHub Actions 自动部署
- 各大加密货币交易所API支持
