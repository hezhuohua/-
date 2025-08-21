#!/usr/bin/env python3
"""
快速修复脚本 - 解决项目中的常见问题
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def backup_file(file_path):
    """备份文件"""
    if os.path.exists(file_path):
        backup_path = f"{file_path}.backup"
        shutil.copy2(file_path, backup_path)
        print(f"✅ 已备份: {backup_path}")
        return backup_path
    return None

def fix_import_issues():
    """修复导入问题"""
    print("🔧 修复导入问题...")

    # 修复backend目录中的导入
    backend_dir = Path("backend")
    if backend_dir.exists():
        # 创建__init__.py文件
        init_file = backend_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            print("✅ 创建了 backend/__init__.py")

        # 修复相对导入
        files_to_fix = [
            "main.py",
            "auth.py",
            "database.py",
            "models.py",
            "schemas.py",
            "exchange_manager.py",
            "prediction_service.py",
            "payment_service.py",
            "rate_limiter.py"
        ]

        for file_name in files_to_fix:
            file_path = backend_dir / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 修复相对导入
                    if 'from .' in content:
                        content = content.replace('from .', 'from ')
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"✅ 修复了 {file_name} 的导入")
                except Exception as e:
                    print(f"⚠️  修复 {file_name} 时出错: {e}")

def fix_database_issues():
    """修复数据库相关问题"""
    print("🗄️  修复数据库问题...")

    # 创建数据库目录
    db_dir = Path(".")
    db_dir.mkdir(exist_ok=True)

    # 检查SQLite数据库
    db_file = db_dir / "crypto_prediction.db"
    if not db_file.exists():
        print("✅ 数据库文件不存在，将在首次运行时自动创建")

def fix_frontend_issues():
    """修复前端相关问题"""
    print("🎨 修复前端问题...")

    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        frontend_dir.mkdir()
        print("✅ 创建了 frontend 目录")

    # 创建前端组件目录
    components_dir = frontend_dir / "components"
    components_dir.mkdir(exist_ok=True)

    # 创建assets目录
    assets_dir = frontend_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    # 创建基础前端应用
    app_py = frontend_dir / "app.py"
    if not app_py.exists():
        app_content = '''#!/usr/bin/env python3
"""
永续合约预测系统前端应用
"""

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json

# 创建Dash应用
app = dash.Dash(__name__, external_stylesheets=[
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'
])

# 应用布局
app.layout = html.Div([
    # 导航栏
    html.Nav([
        html.Div([
            html.H1("永续合约预测系统", className="navbar-brand text-white"),
            html.Div([
                html.Button("登录", id="login-btn", className="btn btn-outline-light mr-2"),
                html.Button("注册", id="register-btn", className="btn btn-primary")
            ], className="ml-auto")
        ], className="navbar-nav d-flex flex-row")
    ], className="navbar navbar-dark bg-dark"),

    # 主要内容
    html.Div([
        # 欢迎区域
        html.Div([
            html.H2("欢迎使用永续合约预测系统", className="text-center mb-4"),
            html.P("基于AI的加密货币价格预测平台", className="text-center text-muted")
        ], className="jumbotron"),

        # 功能区域
        html.Div([
            html.Div([
                html.H3("实时价格", className="card-title"),
                html.P("获取最新加密货币价格", className="card-text"),
                html.Button("查看价格", id="price-btn", className="btn btn-primary")
            ], className="card-body")
        ], className="card mb-3"),

        html.Div([
            html.Div([
                html.H3("AI预测", className="card-title"),
                html.P("使用AI模型预测价格走势", className="card-text"),
                html.Button("开始预测", id="predict-btn", className="btn btn-success")
            ], className="card-body")
        ], className="card mb-3"),

        html.Div([
            html.Div([
                html.H3("会员中心", className="card-title"),
                html.P("管理您的会员账户", className="card-text"),
                html.Button("进入中心", id="member-btn", className="btn btn-info")
            ], className="card-body")
        ], className="card")
    ], className="container mt-4"),

    # 图表区域
    html.Div([
        dcc.Graph(id="price-chart", style={"display": "none"}),
        dcc.Interval(id="interval-component", interval=5*1000, n_intervals=0)
    ])
], className="bg-light min-vh-100")

# 回调函数
@app.callback(
    Output("price-chart", "figure"),
    [Input("price-btn", "n_clicks"),
     Input("interval-component", "n_intervals")]
)
def update_price_chart(n_clicks, n_intervals):
    if n_clicks is None:
        return {}

    # 生成示例数据
    dates = pd.date_range(start=datetime.now() - timedelta(days=7),
                         end=datetime.now(), freq='H')
    prices = np.random.normal(50000, 1000, len(dates))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines+markers',
        name='BTC价格',
        line=dict(color='blue', width=2)
    ))

    fig.update_layout(
        title="BTC价格走势图",
        xaxis_title="时间",
        yaxis_title="价格 (USDT)",
        template="plotly_white"
    )

    return fig

# 启动应用
if __name__ == "__main__":
    print("🚀 启动前端应用...")
    print("📱 访问地址: http://localhost:8080")
    app.run_server(debug=True, host="0.0.0.0", port=8080)
'''

        with open(app_py, 'w', encoding='utf-8') as f:
            f.write(app_content)
        print("✅ 创建了基础前端应用")

def create_directories():
    """创建必要的目录"""
    print("📁 创建必要目录...")

    dirs = ['logs', 'uploads', 'static']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ 创建目录: {dir_name}")

def install_dependencies():
    """安装依赖"""
    print("📦 安装依赖...")

    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                      check=True, capture_output=True)
        print("✅ 依赖安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        print("请手动运行: pip install -r requirements.txt")

def main():
    """主函数"""
    print("🚀 永续合约预测系统快速修复")
    print("=" * 50)

    # 备份重要文件
    print("💾 备份重要文件...")
    files_to_backup = [
        "backend/main.py",
        "backend/models.py",
        "backend/schemas.py"
    ]

    for file_path in files_to_backup:
        if os.path.exists(file_path):
            backup_file(file_path)

    # 执行修复
    fix_import_issues()
    fix_database_issues()
    fix_frontend_issues()
    create_directories()

    print("\n🎉 修复完成！")
    print("=" * 50)
    print("现在您可以运行以下命令启动系统：")
    print("Windows: start.bat")
    print("Linux/Mac: ./start.sh")
    print("或直接运行: python run.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
