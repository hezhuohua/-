#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安代理交易系统后端服务
支持API Key管理、交易执行、数据同步和分润计算
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import hmac
import hashlib
import time
import json
import sqlite3
import os
from datetime import datetime, timedelta
import threading
import schedule
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 配置
class Config:
    BINANCE_MAINNET_URL = "https://fapi.binance.com"
    BINANCE_TESTNET_URL = "https://testnet.binancefuture.com"
    DATABASE_PATH = "trading_system.db"
    SECRET_KEY = "your-secret-key-here"  # 生产环境请使用强密钥

# 数据库初始化
def init_database():
    """初始化数据库表"""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cursor = conn.cursor()

    # 用户API配置表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_api_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            api_key TEXT NOT NULL,
            api_secret TEXT NOT NULL,
            testnet BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 交易记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trade_records (
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
            closed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_api_configs (user_id)
        )
    ''')

    # 分润记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profit_shares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            trade_id INTEGER NOT NULL,
            total_pnl REAL NOT NULL,
            platform_share REAL NOT NULL,
            user_share REAL NOT NULL,
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_api_configs (user_id),
            FOREIGN KEY (trade_id) REFERENCES trade_records (id)
        )
    ''')

    conn.commit()
    conn.close()
    logger.info("数据库初始化完成")

# 币安API工具类
class BinanceAPI:
    def __init__(self, api_key, api_secret, testnet=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = Config.BINANCE_TESTNET_URL if testnet else Config.BINANCE_MAINNET_URL

    def _generate_signature(self, params):
        """生成签名"""
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _make_request(self, method, endpoint, params=None, signed=False):
        """发送API请求"""
        url = f"{self.base_url}{endpoint}"
        headers = {'X-MBX-APIKEY': self.api_key}

        if params is None:
            params = {}

        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)

        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, data=params, headers=headers, timeout=10)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"API请求失败: {e}")
            raise

    def test_connection(self):
        """测试API连接"""
        try:
            result = self._make_request('GET', '/fapi/v2/account', signed=True)
            return {
                'success': True,
                'data': result,
                'message': '连接成功'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': '连接失败'
            }

    def place_order(self, symbol, side, quantity, order_type='MARKET', price=None):
        """下单"""
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }

        if price and order_type == 'LIMIT':
            params['price'] = price
            params['timeInForce'] = 'GTC'

        try:
            result = self._make_request('POST', '/fapi/v1/order', params, signed=True)
            return {
                'success': True,
                'data': result,
                'message': '下单成功'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': '下单失败'
            }

    def get_user_trades(self, symbol=None, limit=100):
        """获取用户交易记录"""
        params = {'limit': limit}
        if symbol:
            params['symbol'] = symbol

        try:
            result = self._make_request('GET', '/fapi/v1/userTrades', params, signed=True)
            return {
                'success': True,
                'data': result,
                'message': '获取交易记录成功'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': '获取交易记录失败'
            }

    def get_position_risk(self):
        """获取持仓风险"""
        try:
            result = self._make_request('GET', '/fapi/v1/positionRisk', signed=True)
            return {
                'success': True,
                'data': result,
                'message': '获取持仓信息成功'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': '获取持仓信息失败'
            }

    def get_market_data(self, symbols=None):
        """获取市场数据（不需要API密钥）"""
        try:
            if symbols is None:
                symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'XRPUSDT']

            # 构建符号列表
            symbols_str = '[' + ','.join([f'"{symbol}"' for symbol in symbols]) + ']'

            # 使用币安官方API获取24小时价格数据
            url = f"{self.base_url}/fapi/v1/ticker/24hr"
            params = {'symbols': symbols_str}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            return {
                'success': True,
                'data': data,
                'message': '获取市场数据成功'
            }
        except Exception as e:
            logger.error(f"获取市场数据失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': '获取市场数据失败'
            }

    def get_price(self, symbol):
        """获取单个币种价格（不需要API密钥）"""
        try:
            url = f"{self.base_url}/fapi/v1/ticker/price"
            params = {'symbol': symbol}

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            return {
                'success': True,
                'data': data,
                'message': '获取价格成功'
            }
        except Exception as e:
            logger.error(f"获取价格失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': '获取价格失败'
            }

    def get_klines(self, symbol, interval='1m', limit=100):
        """获取K线数据（不需要API密钥）"""
        try:
            url = f"{self.base_url}/fapi/v1/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            return {
                'success': True,
                'data': data,
                'message': '获取K线数据成功'
            }
        except Exception as e:
            logger.error(f"获取K线数据失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': '获取K线数据失败'
            }

# 数据库操作类
class DatabaseManager:
    def __init__(self):
        self.db_path = Config.DATABASE_PATH

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def save_api_config(self, user_id, api_key, api_secret, testnet=True):
        """保存用户API配置"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO user_api_configs
                (user_id, api_key, api_secret, testnet, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, api_key, api_secret, testnet))

            conn.commit()
            return True
        except Exception as e:
            logger.error(f"保存API配置失败: {e}")
            return False
        finally:
            conn.close()

    def get_api_config(self, user_id):
        """获取用户API配置"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT api_key, api_secret, testnet
                FROM user_api_configs
                WHERE user_id = ?
            ''', (user_id,))

            result = cursor.fetchone()
            if result:
                return {
                    'api_key': result[0],
                    'api_secret': result[1],
                    'testnet': bool(result[2])
                }
            return None
        finally:
            conn.close()

    def save_trade_record(self, user_id, order_data, take_profit=None, stop_loss=None):
        """保存交易记录"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO trade_records
                (user_id, order_id, symbol, side, price, quantity, status, take_profit, stop_loss)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                order_data['orderId'],
                order_data['symbol'],
                order_data['side'],
                float(order_data['price']),
                float(order_data['executedQty']),
                order_data['status'],
                take_profit,
                stop_loss
            ))

            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"保存交易记录失败: {e}")
            return None
        finally:
            conn.close()

    def get_trade_records(self, user_id, limit=50):
        """获取用户交易记录"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT * FROM trade_records
                WHERE user_id = ?
                ORDER BY executed_at DESC
                LIMIT ?
            ''', (user_id, limit))

            columns = [description[0] for description in cursor.description]
            records = []

            for row in cursor.fetchall():
                record = dict(zip(columns, row))
                record['executed_at'] = record['executed_at']
                records.append(record)

            return records
        finally:
            conn.close()

    def calculate_profit_share(self, user_id, trade_id, total_pnl):
        """计算分润"""
        platform_share = total_pnl * 0.7  # 平台70%
        user_share = total_pnl * 0.3      # 用户30%

        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            # 更新交易记录的盈亏和分润
            cursor.execute('''
                UPDATE trade_records
                SET pnl = ?, platform_share = ?, user_share = ?, closed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (total_pnl, platform_share, user_share, trade_id))

            # 保存分润记录
            cursor.execute('''
                INSERT INTO profit_shares
                (user_id, trade_id, total_pnl, platform_share, user_share)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, trade_id, total_pnl, platform_share, user_share))

            conn.commit()
            return {
                'total_pnl': total_pnl,
                'platform_share': platform_share,
                'user_share': user_share
            }
        except Exception as e:
            logger.error(f"计算分润失败: {e}")
            return None
        finally:
            conn.close()

# 全局变量
db_manager = DatabaseManager()

# API路由
@app.route('/')
def index():
    """主页"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>币安代理交易系统</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>🚀 币安代理交易系统后端服务</h1>
        <p>服务运行正常</p>
        <p>API文档:</p>
        <ul>
            <li>POST /api/config - 保存API配置</li>
            <li>GET /api/config/:user_id - 获取API配置</li>
            <li>POST /api/test - 测试API连接</li>
            <li>POST /api/trade - 执行交易</li>
            <li>GET /api/trades/:user_id - 获取交易记录</li>
            <li>POST /api/sync - 同步交易数据</li>
        </ul>
    </body>
    </html>
    ''')

@app.route('/api/config', methods=['POST'])
def save_api_config():
    """保存API配置"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        api_key = data.get('api_key')
        api_secret = data.get('api_secret')
        testnet = data.get('testnet', True)

        if not all([user_id, api_key, api_secret]):
            return jsonify({'success': False, 'error': '缺少必要参数'}), 400

        success = db_manager.save_api_config(user_id, api_key, api_secret, testnet)

        if success:
            return jsonify({'success': True, 'message': 'API配置保存成功'})
        else:
            return jsonify({'success': False, 'error': '保存失败'}), 500

    except Exception as e:
        logger.error(f"保存API配置异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/config/<user_id>', methods=['GET'])
def get_api_config(user_id):
    """获取API配置"""
    try:
        config = db_manager.get_api_config(user_id)
        if config:
            return jsonify({'success': True, 'data': config})
        else:
            return jsonify({'success': False, 'error': '未找到配置'}), 404

    except Exception as e:
        logger.error(f"获取API配置异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test', methods=['POST'])
def test_api_connection():
    """测试API连接"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        config = db_manager.get_api_config(user_id)
        if not config:
            return jsonify({'success': False, 'error': '未找到API配置'}), 404

        binance_api = BinanceAPI(
            config['api_key'],
            config['api_secret'],
            config['testnet']
        )

        result = binance_api.test_connection()
        return jsonify(result)

    except Exception as e:
        logger.error(f"测试API连接异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/trade', methods=['POST'])
def execute_trade():
    """执行交易"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        symbol = data.get('symbol')
        side = data.get('side')
        quantity = data.get('quantity')
        take_profit = data.get('take_profit')
        stop_loss = data.get('stop_loss')

        if not all([user_id, symbol, side, quantity]):
            return jsonify({'success': False, 'error': '缺少必要参数'}), 400

        config = db_manager.get_api_config(user_id)
        if not config:
            return jsonify({'success': False, 'error': '未找到API配置'}), 404

        binance_api = BinanceAPI(
            config['api_key'],
            config['api_secret'],
            config['testnet']
        )

        # 执行下单
        order_result = binance_api.place_order(symbol, side, quantity)

        if order_result['success']:
            # 保存交易记录
            trade_id = db_manager.save_trade_record(
                user_id,
                order_result['data'],
                take_profit,
                stop_loss
            )

            return jsonify({
                'success': True,
                'message': '交易执行成功',
                'data': {
                    'order_id': order_result['data']['orderId'],
                    'trade_id': trade_id
                }
            })
        else:
            return jsonify(order_result), 400

    except Exception as e:
        logger.error(f"执行交易异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/trades/<user_id>', methods=['GET'])
def get_trade_records(user_id):
    """获取交易记录"""
    try:
        limit = request.args.get('limit', 50, type=int)
        records = db_manager.get_trade_records(user_id, limit)

        return jsonify({
            'success': True,
            'data': records,
            'count': len(records)
        })

    except Exception as e:
        logger.error(f"获取交易记录异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sync', methods=['POST'])
def sync_trade_data():
    """同步交易数据"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        config = db_manager.get_api_config(user_id)
        if not config:
            return jsonify({'success': False, 'error': '未找到API配置'}), 404

        binance_api = BinanceAPI(
            config['api_key'],
            config['api_secret'],
            config['testnet']
        )

        # 同步交易记录
        trades_result = binance_api.get_user_trades()
        if not trades_result['success']:
            return jsonify(trades_result), 400

        # 同步持仓信息
        positions_result = binance_api.get_position_risk()
        if not positions_result['success']:
            return jsonify(positions_result), 400

        return jsonify({
            'success': True,
            'message': '数据同步成功',
            'data': {
                'trades': trades_result['data'],
                'positions': positions_result['data']
            }
        })

    except Exception as e:
        logger.error(f"同步交易数据异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/profit-share', methods=['POST'])
def calculate_profit_share():
    """计算分润"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        trade_id = data.get('trade_id')
        total_pnl = data.get('total_pnl')

        if not all([user_id, trade_id, total_pnl]):
            return jsonify({'success': False, 'error': '缺少必要参数'}), 400

        result = db_manager.calculate_profit_share(user_id, trade_id, total_pnl)

        if result:
            return jsonify({
                'success': True,
                'message': '分润计算成功',
                'data': result
            })
        else:
            return jsonify({'success': False, 'error': '分润计算失败'}), 500

    except Exception as e:
        logger.error(f"计算分润异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    """获取市场数据（不需要API密钥）"""
    try:
        symbols = request.args.get('symbols', 'BTCUSDT,ETHUSDT,BNBUSDT,SOLUSDT,XRPUSDT')
        symbol_list = [s.strip() for s in symbols.split(',')]

        # 创建币安API实例（不需要API密钥）
        binance_api = BinanceAPI('', '', testnet=False)

        result = binance_api.get_market_data(symbol_list)

        if result['success']:
            return jsonify({
                'success': True,
                'message': '获取市场数据成功',
                'data': result['data']
            })
        else:
            return jsonify({'success': False, 'error': result['message']}), 500

    except Exception as e:
        logger.error(f"获取市场数据异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/price/<symbol>', methods=['GET'])
def get_price(symbol):
    """获取单个币种价格（不需要API密钥）"""
    try:
        # 创建币安API实例（不需要API密钥）
        binance_api = BinanceAPI('', '', testnet=False)

        result = binance_api.get_price(symbol.upper())

        if result['success']:
            return jsonify({
                'success': True,
                'message': '获取价格成功',
                'data': result['data']
            })
        else:
            return jsonify({'success': False, 'error': result['message']}), 500

    except Exception as e:
        logger.error(f"获取价格异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/klines/<symbol>', methods=['GET'])
def get_klines(symbol):
    """获取K线数据（不需要API密钥）"""
    try:
        interval = request.args.get('interval', '1m')
        limit = int(request.args.get('limit', 100))

        # 创建币安API实例（不需要API密钥）
        binance_api = BinanceAPI('', '', testnet=False)

        result = binance_api.get_klines(symbol.upper(), interval, limit)

        if result['success']:
            return jsonify({
                'success': True,
                'message': '获取K线数据成功',
                'data': result['data']
            })
        else:
            return jsonify({'success': False, 'error': result['message']}), 500

    except Exception as e:
        logger.error(f"获取K线数据异常: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# 定时任务
def sync_all_users_data():
    """定时同步所有用户数据"""
    logger.info("开始定时同步用户数据...")

    conn = db_manager.get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT user_id FROM user_api_configs')
        user_ids = [row[0] for row in cursor.fetchall()]

        for user_id in user_ids:
            try:
                config = db_manager.get_api_config(user_id)
                if config:
                    binance_api = BinanceAPI(
                        config['api_key'],
                        config['api_secret'],
                        config['testnet']
                    )

                    # 同步交易记录
                    trades_result = binance_api.get_user_trades()
                    if trades_result['success']:
                        logger.info(f"用户 {user_id} 交易记录同步成功")

                    # 同步持仓信息
                    positions_result = binance_api.get_position_risk()
                    if positions_result['success']:
                        logger.info(f"用户 {user_id} 持仓信息同步成功")

            except Exception as e:
                logger.error(f"同步用户 {user_id} 数据失败: {e}")

    except Exception as e:
        logger.error(f"定时同步任务失败: {e}")
    finally:
        conn.close()

def run_scheduler():
    """运行定时任务"""
    schedule.every(5).minutes.do(sync_all_users_data)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    # 初始化数据库
    init_database()

    # 启动定时任务线程
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    # 启动Flask应用
    logger.info("币安代理交易系统后端服务启动...")
    app.run(host='0.0.0.0', port=5000, debug=True)
