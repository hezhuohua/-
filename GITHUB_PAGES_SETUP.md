# 🌐 GitHub Pages 设置指南

## 📋 启用GitHub Pages步骤

### 1. 访问仓库设置
1. 打开您的GitHub仓库：https://github.com/hezhuohua/-
2. 点击仓库顶部的 **Settings** 标签
3. 在左侧菜单中找到 **Pages** 选项

### 2. 配置Pages设置
1. 在 **Source** 部分选择：**Deploy from a branch**
2. 在 **Branch** 下拉菜单中选择：**gh-pages**
3. 文件夹选择：**/ (root)**
4. 点击 **Save** 保存设置

### 3. 等待部署完成
- GitHub会自动开始部署过程
- 通常需要1-5分钟完成
- 部署完成后会显示绿色的✅标记

### 4. 访问您的网站
部署完成后，您的网站将在以下地址可用：
```
https://hezhuohua.github.io/-
```

## 🔧 自动部署工作流

### GitHub Actions配置
我们已经为您配置了自动部署工作流：

**文件位置**: `.github/workflows/deploy.yml`

**触发条件**:
- 推送到 `master` 分支
- 创建Pull Request到 `master` 分支

**部署流程**:
1. 检出代码
2. 设置Node.js和Python环境
3. 安装依赖
4. 构建项目
5. 部署到GitHub Pages

### 部署状态监控
您可以在以下位置查看部署状态：
- **Actions页面**: https://github.com/hezhuohua/-/actions
- **部署徽章**: 在README.md中显示

## 🚀 快速部署命令

### Windows用户
```batch
# 双击运行
deploy.bat
```

### Linux/Mac用户
```bash
chmod +x deploy.sh
./deploy.sh
```

### 手动Git命令
```bash
git add .
git commit -m "更新内容"
git push origin master
```

## 🔍 故障排除

### 常见问题

1. **Pages没有启用**
   - 确保在Settings > Pages中正确配置了源分支

2. **部署失败**
   - 检查Actions页面的错误日志
   - 确保所有文件都已正确提交

3. **网站无法访问**
   - 等待5-10分钟让DNS传播
   - 检查浏览器缓存

4. **404错误**
   - 我们已配置404页面自动重定向到主页
   - 确保index.html文件存在

### 检查部署状态
```bash
# 查看最近的提交
git log --oneline -5

# 查看远程分支
git branch -r

# 强制推送（谨慎使用）
git push origin master --force
```

## 📊 部署信息

每次部署都会生成部署信息文件：
- **文件位置**: `/deploy-info.txt`
- **包含内容**: 部署时间、提交ID等

## 🎯 下一步

1. ✅ 启用GitHub Pages
2. ✅ 等待首次部署完成
3. ✅ 访问您的网站
4. ✅ 测试所有功能
5. ✅ 享受自动部署的便利！

---

**🎉 恭喜！您的永续合约预测系统现在已经可以通过互联网访问了！**
