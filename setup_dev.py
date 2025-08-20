#!/usr/bin/env python3
"""
开发环境快速设置脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_step(step, message):
    """打印步骤信息"""
    print(f"\n{'='*50}")
    print(f"步骤 {step}: {message}")
    print('='*50)

def run_command(command, description):
    """运行命令并处理错误"""
    print(f"执行: {description}")
    print(f"命令: {command}")

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} 成功")
        if result.stdout:
            print(f"输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} 失败")
        print(f"错误: {e.stderr}")
        return False

def check_python_version():
    """检查Python版本"""
    print_step(1, "检查Python版本")

    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")

    if version < (3, 8):
        print("✗ 需要Python 3.8或更高版本")
        return False

    print("✓ Python版本符合要求")
    return True

def create_virtual_environment():
    """创建虚拟环境"""
    print_step(2, "创建虚拟环境")

    if os.path.exists("venv"):
        print("虚拟环境已存在，跳过创建")
        return True

    return run_command("python -m venv venv", "创建虚拟环境")

def activate_virtual_environment():
    """激活虚拟环境指导"""
    print_step(3, "激活虚拟环境")

    system = platform.system()
    if system == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"

    print(f"请手动执行以下命令激活虚拟环境:")
    print(f"  {activate_cmd}")
    print("\n激活后请重新运行此脚本继续安装依赖")

    # 检查是否在虚拟环境中
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✓ 检测到虚拟环境已激活")
        return True
    else:
        print("⚠ 虚拟环境未激活，请先激活虚拟环境")
        return False

def install_dependencies():
    """安装依赖"""
    print_step(4, "安装Python依赖")

    if not os.path.exists("requirements.txt"):
        print("✗ requirements.txt 文件不存在")
        return False

    return run_command("pip install -r requirements.txt", "安装Python依赖")

def create_env_file():
    """创建环境配置文件"""
    print_step(5, "创建环境配置文件")

    if os.path.exists(".env"):
        print(".env 文件已存在，跳过创建")
        return True

    env_content = """# 开发环境配置
DEBUG=True
DATABASE_URL=sqlite:///./crypto_prediction_dev.db
REDIS_URL=redis://localhost:6379/1
SECRET_KEY=dev-secret-key-change-in-production
DEEPSEEK_API_KEY=your-deepseek-api-key

# 服务器配置
HOST=0.0.0.0
PORT=8000
"""

    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✓ .env 文件创建成功")
        return True
    except Exception as e:
        print(f"✗ .env 文件创建失败: {e}")
        return False

def create_directories():
    """创建必要的目录"""
    print_step(6, "创建项目目录")

    directories = [
        "uploads",
        "uploads/qrcodes",
        "uploads/proofs",
        "static",
        "logs"
    ]

    success = True
    for directory in directories:
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✓ 创建目录: {directory}")
        except Exception as e:
            print(f"✗ 创建目录失败 {directory}: {e}")
            success = False

    return success

def run_tests():
    """运行基础测试"""
    print_step(7, "运行基础测试")

    return run_command("python -m pytest tests/test_basic.py -v", "运行基础测试")

def check_vscode_config():
    """检查VSCode配置"""
    print_step(8, "检查VSCode配置")

    vscode_files = [
        ".vscode/settings.json",
        ".vscode/launch.json",
        ".vscode/tasks.json",
        ".vscode/extensions.json"
    ]

    all_exist = True
    for file_path in vscode_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} 存在")
        else:
            print(f"✗ {file_path} 不存在")
            all_exist = False

    if all_exist:
        print("\n✓ VSCode配置文件完整")
        print("建议安装推荐的VSCode扩展以获得最佳开发体验")

    return all_exist

def check_mcp_config():
    """检查MCP配置示例"""
    print_step(9, "检查MCP配置")

    mcp_example = ".vscode/mcp_config_example.json"
    if os.path.exists(mcp_example):
        print(f"✓ MCP配置示例文件存在: {mcp_example}")
        print("📝 MCP配置说明:")
        print("   1. 查看 .vscode/mcp_config_example.json 文件")
        print("   2. 获取TestSprite API密钥")
        print("   3. 在VSCode中配置MCP服务器")
        return True
    else:
        print(f"✗ MCP配置示例文件不存在: {mcp_example}")
        return False

def print_next_steps():
    """打印后续步骤"""
    print_step("完成", "开发环境设置完成")

    print("🎉 开发环境设置成功！")
    print("\n📋 后续步骤:")
    print("1. 在VSCode中打开项目文件夹")
    print("2. 安装推荐的VSCode扩展")
    print("3. 配置MCP服务器（强烈推荐）:")
    print("   📄 方法一 - 使用VSCode命令:")
    print("     - Cmd/Ctrl + Shift + P")
    print("     - 运行 'MCP：添加服务器'")
    print("     - 选择 '命令 (stdio)'")
    print("     - 输入: npx @testsprite/testsprite-mcp@latest")
    print("     - 标识符: TestSprite")
    print("     - 添加API_KEY环境变量")
    print("   📄 方法二 - 手动配置:")
    print("     - 查看 .vscode/mcp_config_example.json")
    print("     - 复制配置到MCP设置文件")
    print("     - 替换API密钥")
    print("\n🔑 获取API密钥:")
    print("   - 访问 https://testsprite.com")
    print("   - 注册并获取API密钥")
    print("\n🚀 启动项目:")
    print("   python run_server.py")
    print("\n📖 查看开发文档:")
    print("   DEVELOPMENT.md")
    print("\n💡 MCP功能:")
    print("   - 智能代码补全")
    print("   - 错误检测和修复")
    print("   - 代码重构建议")
    print("   - 自动文档生成")

def main():
    """主函数"""
    print("🚀 永续合约预测系统 - 开发环境设置")
    print("=" * 60)

    steps = [
        check_python_version,
        create_virtual_environment,
        activate_virtual_environment,
        install_dependencies,
        create_env_file,
        create_directories,
        run_tests,
        check_vscode_config,
        check_mcp_config
    ]

    for i, step in enumerate(steps, 1):
        if not step():
            print(f"\n❌ 步骤 {i} 失败，请检查错误信息并重试")
            sys.exit(1)

    print_next_steps()

if __name__ == "__main__":
    main()
