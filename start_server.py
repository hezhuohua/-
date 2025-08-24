#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安代理交易系统启动脚本
"""

import os
import sys
import logging
from server import app, init_database
from config import get_config

def setup_logging():
    """设置日志配置"""
    config = get_config()

    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """主函数"""
    # 设置日志
    setup_logging()

    # 获取配置
    config = get_config()

    # 初始化数据库
    init_database()

    # 启动服务器
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))

    print("🚀 币安代理交易系统启动中...")
    print(f"📊 环境: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"🌐 地址: http://{host}:{port}")
    print(f"📝 日志级别: {config.LOG_LEVEL}")
    print(f"💾 数据库: {config.DATABASE_PATH}")

    if config.DEBUG:
        print("🔧 调试模式已启用")

    try:
        app.run(
            host=host,
            port=port,
            debug=config.DEBUG,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
