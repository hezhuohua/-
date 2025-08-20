#!/bin/bash

# 永续合约预测系统部署脚本
echo "🚀 开始部署永续合约预测系统..."

# 检查Git状态
echo "📋 检查Git状态..."
git status

# 添加所有更改
echo "📦 添加文件到Git..."
git add .

# 提示用户输入提交信息
echo "💬 请输入提交信息 (按Enter使用默认信息):"
read commit_message

if [ -z "$commit_message" ]; then
    commit_message="更新永续合约预测系统 - $(date '+%Y-%m-%d %H:%M:%S')"
fi

# 提交更改
echo "💾 提交更改..."
git commit -m "$commit_message"

# 推送到GitHub
echo "🌐 推送到GitHub..."
git push origin master

echo "✅ 部署完成！"
echo "🔗 GitHub仓库: https://github.com/hezhuohua/-"
echo "🌐 GitHub Pages: https://hezhuohua.github.io/-"
echo "⏰ 请等待1-2分钟让GitHub Actions完成自动部署"

# 检查GitHub Actions状态
echo "📊 您可以在以下链接查看部署状态:"
echo "https://github.com/hezhuohua/-/actions"
