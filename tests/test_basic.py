"""
基础功能测试
"""
import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_python_version():
    """测试Python版本"""
    assert sys.version_info >= (3, 8), "需要Python 3.8或更高版本"

def test_imports():
    """测试关键模块导入"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        assert True
    except ImportError as e:
        pytest.fail(f"导入失败: {e}")

def test_project_structure():
    """测试项目结构"""
    project_root = os.path.join(os.path.dirname(__file__), '..')

    # 检查关键文件是否存在
    required_files = [
        'requirements.txt',
        'README.md',
        'index.html',
        'demo.html',
        'run_server.py'
    ]

    for file_name in required_files:
        file_path = os.path.join(project_root, file_name)
        assert os.path.exists(file_path), f"缺少文件: {file_name}"

    # 检查关键目录是否存在
    required_dirs = [
        'backend',
        '.vscode',
        'tests'
    ]

    for dir_name in required_dirs:
        dir_path = os.path.join(project_root, dir_name)
        assert os.path.exists(dir_path), f"缺少目录: {dir_name}"

def test_backend_modules():
    """测试后端模块"""
    try:
        from backend import models, auth, database, schemas, rate_limiter
        assert True
    except ImportError as e:
        pytest.fail(f"后端模块导入失败: {e}")

def test_environment_variables():
    """测试环境变量配置"""
    import os

    # 检查是否有.env.example文件
    assert os.path.exists(".env.example"), "缺少 .env.example 文件"

    # 检查关键环境变量（如果设置了的话）
    secret_key = os.getenv("SECRET_KEY")
    if secret_key:
        assert len(secret_key) >= 32, "SECRET_KEY长度应至少32字符"

def test_security_imports():
    """测试安全相关模块导入"""
    try:
        from backend.schemas import UserRegister, UserLogin, PredictionRequest
        from backend.rate_limiter import RateLimiter, check_rate_limit
        assert True
    except ImportError as e:
        pytest.fail(f"安全模块导入失败: {e}")

def test_configuration():
    """测试配置文件"""
    project_root = os.path.join(os.path.dirname(__file__), '..')

    # 检查VSCode配置文件
    vscode_files = [
        '.vscode/settings.json',
        '.vscode/launch.json',
        '.vscode/tasks.json',
        '.vscode/extensions.json'
    ]

    for file_name in vscode_files:
        file_path = os.path.join(project_root, file_name)
        assert os.path.exists(file_path), f"缺少VSCode配置文件: {file_name}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
