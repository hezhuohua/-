#!/bin/bash

echo "========================================"
echo "  永续合约预测系统启动脚本"
echo "========================================"
echo

# 检查Python环境
echo "正在检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.8+"
    exit 1
fi

echo "✅ Python环境检查通过"
echo

# 检查pip
echo "正在检查pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到pip3，请先安装pip"
    exit 1
fi

echo "✅ pip检查通过"
echo

# 安装依赖
echo "正在安装依赖..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✅ 依赖安装完成"
echo

# 启动系统
echo "正在启动系统..."
python3 run.py
