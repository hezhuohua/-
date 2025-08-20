#!/usr/bin/env python3
"""
快速修复脚本 - 自动修复一些常见的代码问题
"""

import os
import re
import shutil
from pathlib import Path

def backup_files():
    """备份原始文件"""
    backup_dir = Path("backup_before_fixes")
    backup_dir.mkdir(exist_ok=True)
    
    files_to_backup = [
        "backend/auth.py",
        "backend/prediction_service.py",
        "backend/main.py",
        "requirements.txt"
    ]
    
    for file_path in files_to_backup:
        if os.path.exists(file_path):
            shutil.copy2(file_path, backup_dir / Path(file_path).name)
            print(f"✓ 备份文件: {file_path}")

def fix_hardcoded_secrets():
    """修复硬编码的敏感信息"""
    print("\n🔧 修复硬编码敏感信息...")
    
    # 修复 auth.py
    auth_file = "backend/auth.py"
    if os.path.exists(auth_file):
        with open(auth_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换硬编码的SECRET_KEY
        content = re.sub(
            r'SECRET_KEY = "your-secret-key-here-change-in-production"',
            '''import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required")''',
            content
        )
        
        # 添加导入语句（如果不存在）
        if "from dotenv import load_dotenv" not in content:
            content = "import os\nfrom dotenv import load_dotenv\n" + content
        
        with open(auth_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ 修复 {auth_file} 中的硬编码SECRET_KEY")
    
    # 修复 prediction_service.py
    prediction_file = "backend/prediction_service.py"
    if os.path.exists(prediction_file):
        with open(prediction_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换硬编码的API密钥
        content = re.sub(
            r'self\.deepseek_api_key = "your-deepseek-api-key"',
            '''self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.deepseek_api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is required")''',
            content
        )
        
        # 添加导入语句
        if "import os" not in content:
            content = "import os\n" + content
        
        with open(prediction_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ 修复 {prediction_file} 中的硬编码API密钥")

def add_missing_dependencies():
    """添加缺失的依赖"""
    print("\n📦 添加缺失的依赖...")
    
    requirements_file = "requirements.txt"
    
    # 读取现有依赖
    existing_deps = set()
    if os.path.exists(requirements_file):
        with open(requirements_file, 'r') as f:
            existing_deps = {line.strip().split('==')[0].split('>=')[0] for line in f if line.strip()}
    
    # 需要添加的依赖
    new_dependencies = [
        "python-dotenv>=1.0.0",
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0",
        "pytest-cov>=4.0.0",
        "httpx>=0.24.0",
        "pytest-mock>=3.10.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "isort>=5.12.0"
    ]
    
    deps_to_add = []
    for dep in new_dependencies:
        dep_name = dep.split('>=')[0]
        if dep_name not in existing_deps:
            deps_to_add.append(dep)
    
    if deps_to_add:
        with open(requirements_file, 'a') as f:
            f.write('\n# 开发和测试依赖\n')
            for dep in deps_to_add:
                f.write(f"{dep}\n")
        
        print(f"✓ 添加了 {len(deps_to_add)} 个新依赖")
        for dep in deps_to_add:
            print(f"  - {dep}")
    else:
        print("✓ 所有依赖已存在")

def create_env_template():
    """创建环境变量模板"""
    print("\n🔧 创建环境变量模板...")
    
    env_template = """.env.example
# 环境变量配置模板
# 复制此文件为 .env 并填入实际值

# 安全配置
SECRET_KEY=your-very-secure-secret-key-here-at-least-32-characters
CSRF_SECRET_KEY=your-csrf-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# 数据库配置
DATABASE_URL=sqlite:///./crypto_prediction.db

# API配置
DEEPSEEK_API_KEY=your-deepseek-api-key-here

# Redis配置（可选）
REDIS_URL=redis://localhost:6379

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=False

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# 交易所API配置（可选）
BINANCE_API_KEY=your-binance-api-key
BINANCE_SECRET_KEY=your-binance-secret-key
OKX_API_KEY=your-okx-api-key
OKX_SECRET_KEY=your-okx-secret-key
"""
    
    with open(".env.example", 'w', encoding='utf-8') as f:
        f.write(env_template)
    
    print("✓ 创建 .env.example 模板文件")

def remove_unused_imports():
    """移除未使用的导入"""
    print("\n🧹 清理未使用的导入...")
    
    python_files = [
        "backend/exchange_manager.py",
        "backend/prediction_service.py",
        "backend/payment_service.py"
    ]
    
    for file_path in python_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 移除明显未使用的导入（简单检查）
            lines = content.split('\n')
            cleaned_lines = []
            
            for line in lines:
                # 检查是否为导入语句
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    # 简单检查：如果导入的模块在文件中被使用
                    import_match = re.search(r'import\s+(\w+)', line)
                    if import_match:
                        module_name = import_match.group(1)
                        # 如果模块名在文件其他地方出现，保留导入
                        if module_name in content.replace(line, ''):
                            cleaned_lines.append(line)
                        else:
                            print(f"  移除未使用的导入: {line.strip()} from {file_path}")
                    else:
                        cleaned_lines.append(line)
                else:
                    cleaned_lines.append(line)
            
            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(cleaned_lines))

def create_gitignore():
    """创建.gitignore文件"""
    print("\n📝 创建.gitignore文件...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env
.env.local
.env.development
.env.production

# Database
*.db
*.sqlite
*.sqlite3

# Logs
logs/
*.log

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Uploads
uploads/
static/uploads/

# Cache
.pytest_cache/
.coverage
htmlcov/

# Backup
backup_before_fixes/

# Node modules (if any)
node_modules/
"""
    
    with open(".gitignore", 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✓ 创建 .gitignore 文件")

def main():
    """主函数"""
    print("🔧 永续合约预测系统 - 快速修复脚本")
    print("=" * 60)
    
    # 备份文件
    backup_files()
    
    # 执行修复
    fix_hardcoded_secrets()
    add_missing_dependencies()
    create_env_template()
    remove_unused_imports()
    create_gitignore()
    
    print("\n" + "=" * 60)
    print("✅ 快速修复完成！")
    print("\n📋 后续步骤:")
    print("1. 复制 .env.example 为 .env 并填入实际配置")
    print("2. 安装新的依赖: pip install -r requirements.txt")
    print("3. 运行测试验证修复: pytest")
    print("4. 查看详细修复指南:")
    print("   - SECURITY_FIXES.md (安全问题)")
    print("   - PERFORMANCE_FIXES.md (性能优化)")
    print("   - TEST_IMPROVEMENTS.md (测试改进)")
    print("\n⚠️ 注意: 原始文件已备份到 backup_before_fixes/ 目录")

if __name__ == "__main__":
    main()
