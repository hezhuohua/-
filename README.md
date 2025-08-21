# 永续合约预测系统

基于AI的加密货币永续合约价格预测系统，提供实时价格预测、用户管理和支付功能。

## 功能特性

- 🔮 AI驱动的价格预测
- 👥 用户注册和认证系统
- 💳 支付和订单管理
- 📊 实时数据可视化
- 🔒 安全认证和权限控制
- 📱 响应式Web界面

## 技术架构

### 后端
- **FastAPI**: 高性能异步Web框架
- **SQLAlchemy**: ORM数据库操作
- **Redis**: 缓存和会话管理
- **JWT**: 用户认证
- **WebSocket**: 实时数据推送

### 前端
- **Dash**: 数据可视化框架
- **Bootstrap**: 响应式UI组件
- **Plotly**: 交互式图表
- **WebSocket**: 实时数据更新

### AI/ML
- **Scikit-learn**: 机器学习算法
- **Pandas/Numpy**: 数据处理
- **Matplotlib/Seaborn**: 数据可视化

## 快速开始

### 环境要求
- Python 3.8+
- Redis 6.0+
- SQLite 3.x

### 安装依赖
```bash
pip install -r requirements.txt
```

### 环境配置
1. 复制 `.env.example` 为 `.env`
2. 修改配置参数

### 启动服务
```bash
# 启动Redis
redis-server

# 启动后端
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 启动前端
cd frontend
python app.py
```

## 项目结构

```
├── backend/                 # 后端服务
│   ├── main.py             # 主应用入口
│   ├── models.py           # 数据模型
│   ├── schemas.py          # 数据验证
│   ├── auth.py             # 认证模块
│   ├── database.py         # 数据库配置
│   ├── exchange_manager.py # 交易所数据管理
│   ├── prediction_service.py # 预测服务
│   ├── payment_service.py  # 支付服务
│   └── rate_limiter.py    # 速率限制
├── frontend/               # 前端应用
│   ├── app.py             # Dash应用入口
│   ├── components/        # UI组件
│   └── assets/            # 静态资源
├── static/                 # 静态文件
├── uploads/                # 上传文件
├── logs/                   # 日志文件
├── requirements.txt        # Python依赖
└── README.md              # 项目说明
```

## API文档

启动后端服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 主要功能模块

### 1. 用户管理
- 用户注册/登录
- JWT token认证
- 用户信息管理

### 2. 预测服务
- 实时价格数据获取
- AI模型预测
- 预测结果展示

### 3. 支付系统
- 订单创建
- 支付处理
- 使用记录

### 4. 数据可视化
- 价格走势图
- 预测结果对比
- 实时数据更新

## 开发说明

### 代码规范
- 使用Black进行代码格式化
- 遵循PEP 8编码规范
- 添加适当的类型注解

### 测试
```bash
# 运行测试
pytest

# 代码覆盖率
pytest --cov=.
```

### 部署
- 使用Gunicorn作为WSGI服务器
- 配置Nginx反向代理
- 使用Supervisor管理进程

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者
