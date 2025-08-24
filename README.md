# 🚀 永续合约预测系统 - 币安代理交易版

## 📋 系统概述

这是一个完整的永续合约预测和代理交易系统，集成了AI预测信号、币安API代理交易、自动分润等功能。

### 🎯 核心功能

- **AI预测信号**: 基于技术指标的智能预测
- **币安API代理交易**: 用户授权，平台代为执行交易
- **自动分润**: 7:3分润机制（平台70%，用户30%）
- **风险控制**: 多重安全机制和风险限制
- **实时监控**: 交易记录和盈亏统计

## 🏗️ 系统架构

```
前端 (HTML/CSS/JS)
    ↓
后端 API (Python Flask)
    ↓
币安API (Binance Futures)
    ↓
SQLite数据库
```

## 📁 文件结构

```
永续合约预测系统开发/
├── 币安代理交易系统.html    # 前端界面
├── server.py               # 后端API服务
├── config.py               # 配置文件
├── start_server.py         # 启动脚本
├── requirements.txt        # Python依赖
├── README.md              # 说明文档
└── trading_system.db      # 数据库文件（自动生成）
```

## 🚀 快速开始

### 1. 环境准备

确保已安装Python 3.8+

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动后端服务

```bash
python start_server.py
```

### 4. 访问前端

打开 `币安代理交易系统.html` 文件，或通过HTTP服务器访问：

```bash
python -m http.server 8080
```

然后访问: http://localhost:8080/币安代理交易系统.html

## 🔧 配置说明

### 环境变量

```bash
# 开发环境
export FLASK_ENV=development
export DEBUG=True

# 生产环境
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export API_KEY_ENCRYPTION_KEY=your-encryption-key
```

### 币安API配置

1. 登录币安官网
2. 进入API管理页面
3. 创建新的API Key
4. **重要**: 只勾选"交易"和"查询"权限，**禁止提现**
5. 建议设置IP白名单

## 📊 功能模块

### 1. API配置管理

- 安全的API Key存储
- 连接测试功能
- 支持测试网络

### 2. 预测信号

- 实时价格监控
- AI技术分析
- 多币种支持

### 3. 交易执行

- 一键下单功能
- 自动杠杆设置
- 止盈止损管理

### 4. 数据同步

- 定时同步交易记录
- 持仓信息更新
- 盈亏统计

### 5. 分润系统

- 自动7:3分润
- 实时计算
- 历史记录

## 🔒 安全机制

### API安全

- API Key加密存储
- 禁止提现权限
- IP白名单支持

### 风险控制

- 最大仓位限制
- 每日交易次数限制
- 杠杆倍数控制
- 自动止损机制

### 数据安全

- 数据库加密
- 日志记录
- 异常监控

## 📈 使用流程

### 用户端

1. **注册/登录** 平台账号
2. **绑定币安API** (仅交易+查询权限)
3. **查看预测信号** (AI分析结果)
4. **点击交易按钮** (一键下单)
5. **查看交易记录** (实时同步)
6. **获得分润收益** (自动计算)

### 平台端

1. **接收预测信号** (AI/技术分析)
2. **用户授权交易** (API Key验证)
3. **执行币安下单** (代理交易)
4. **同步交易数据** (定时任务)
5. **计算分润** (7:3分配)

## 🔧 API接口

### 基础接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 系统状态页面 |
| `/api/config` | POST | 保存API配置 |
| `/api/config/<user_id>` | GET | 获取API配置 |
| `/api/test` | POST | 测试API连接 |

### 交易接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/trade` | POST | 执行交易 |
| `/api/trades/<user_id>` | GET | 获取交易记录 |
| `/api/sync` | POST | 同步交易数据 |
| `/api/profit-share` | POST | 计算分润 |

## 📊 数据库设计

### 用户API配置表 (user_api_configs)

```sql
CREATE TABLE user_api_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT UNIQUE NOT NULL,
    api_key TEXT NOT NULL,
    api_secret TEXT NOT NULL,
    testnet BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 交易记录表 (trade_records)

```sql
CREATE TABLE trade_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    order_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    side TEXT NOT NULL,
    price REAL NOT NULL,
    quantity REAL NOT NULL,
    status TEXT NOT NULL,
    take_profit REAL,
    stop_loss REAL,
    pnl REAL DEFAULT 0,
    platform_share REAL DEFAULT 0,
    user_share REAL DEFAULT 0,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP
);
```

### 分润记录表 (profit_shares)

```sql
CREATE TABLE profit_shares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    trade_id INTEGER NOT NULL,
    total_pnl REAL NOT NULL,
    platform_share REAL NOT NULL,
    user_share REAL NOT NULL,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## ⚠️ 风险提示

1. **投资有风险，入市需谨慎**
2. **请合理控制仓位，避免过度杠杆**
3. **建议先使用测试网络熟悉系统**
4. **定期检查API权限设置**
5. **关注市场风险，及时调整策略**

## 🔄 更新日志

### v1.0.0 (2025-01-XX)
- 初始版本发布
- 基础交易功能
- API配置管理
- 分润系统

## 📞 技术支持

如有问题，请检查：
1. API Key权限设置
2. 网络连接状态
3. 系统日志文件
4. 数据库连接

## 📄 许可证

本项目仅供学习和研究使用，请遵守相关法律法规。

---

**🎯 下一步计划**
- [ ] 增加更多技术指标
- [ ] 优化AI预测算法
- [ ] 添加移动端支持
- [ ] 增强风险控制
- [ ] 支持更多交易所
