#!/bin/bash

echo "========================================"
echo "  永续合约预测系统 - Bash启动脚本"
echo "========================================"
echo

# 检查Python环境
echo "正在检查Python环境..."
if ! command -v python &> /dev/null; then
    if ! command -v python3 &> /dev/null; then
        echo "❌ 未找到Python，请先安装Python 3.8+"
        exit 1
    else
        PYTHON_CMD="python3"
    fi
else
    PYTHON_CMD="python"
fi

echo "✅ Python环境检查通过 (使用: $PYTHON_CMD)"
echo

# 检查pip
echo "正在检查pip..."
if ! command -v pip &> /dev/null; then
    if ! command -v pip3 &> /dev/null; then
        echo "❌ 未找到pip，请先安装pip"
        exit 1
    else
        PIP_CMD="pip3"
    fi
else
    PIP_CMD="pip"
fi

echo "✅ pip检查通过 (使用: $PIP_CMD)"
echo

# 安装依赖
echo "正在安装依赖..."
$PIP_CMD install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✅ 依赖安装完成"
echo

# 启动后端服务
echo "🚀 启动后端服务..."
echo "📊 服务地址: http://localhost:5000"
echo "🌐 前端地址: http://localhost:8080/index.html"
echo

# 在后台启动后端服务
$PYTHON_CMD start_server.py &
BACKEND_PID=$!

# 等待3秒让后端启动
sleep 3

# 启动前端服务
echo "🌐 启动前端服务..."
$PYTHON_CMD -m http.server 8080 &
FRONTEND_PID=$!

echo
echo "✅ 系统启动完成！"
echo
echo "📋 使用说明:"
echo "1. 后端API服务运行在: http://localhost:5000"
echo "2. 前端界面访问: http://localhost:8080/index.html"
echo "3. 请确保币安API Key已正确配置"
echo "4. 建议先使用测试网络熟悉系统"
echo
echo "⚠️  重要提醒:"
echo "- 请确保API Key仅勾选'交易'和'查询'权限"
echo "- 禁止提现权限，确保资金安全"
echo "- 建议设置IP白名单限制"
echo
echo "按 Ctrl+C 停止服务..."

# 等待用户中断
trap "echo '正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
