import asyncio
import websockets
import json
import logging
import time
from typing import Dict, List, Optional
import aiohttp
from datetime import datetime
import random

class MarketData:
    def __init__(self):
        self.symbol = ""
        self.exchange = ""
        self.price = 0.0
        self.volume_24h = 0.0
        self.change_24h = 0.0
        self.change_percent_24h = 0.0
        self.high_24h = 0.0
        self.low_24h = 0.0
        self.funding_rate = 0.0
        self.open_interest = 0.0
        self.timestamp = 0
        
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'exchange': self.exchange,
            'price': self.price,
            'volume_24h': self.volume_24h,
            'change_24h': self.change_24h,
            'change_percent_24h': self.change_percent_24h,
            'high_24h': self.high_24h,
            'low_24h': self.low_24h,
            'funding_rate': self.funding_rate,
            'open_interest': self.open_interest,
            'timestamp': self.timestamp
        }

class ExchangeDataManager:
    def __init__(self):
        self.market_data: Dict[str, Dict[str, MarketData]] = {}
        self.websocket_connections = {}
        self.symbols = ['BTCUSDT', 'ETHUSDT']
        self.connection_status = {}  # 连接状态跟踪
        self.last_update_time = {}   # 最后更新时间
        self.reconnect_attempts = {}  # 重连尝试次数
        self.heartbeat_times = {}     # 心跳时间
        self.connection_logs = {}     # 连接日志记录
        
        # 交易所配置 - 增强容错能力
        self.exchanges_config = {
            'binance': {
                'name': '币安',
                'websocket': 'wss://stream.binance.com:9443/ws/',
                'rest_api': 'https://api.binance.com/api/v3/',
                'backup_ws': 'wss://stream.binancefuture.com/ws/',  # 备用WebSocket
                'priority': 1,
                'reconnect_delay': 3,  # 重连延迟(秒)
                'max_reconnect_attempts': 10,
                'heartbeat_timeout': 30  # 心跳超时(秒)
            },
            'okx': {
                'name': 'OKX',
                'websocket': 'wss://ws.okx.com:8443/ws/v5/public',
                'rest_api': 'https://www.okx.com/api/v5/',
                'backup_ws': 'wss://wsaws.okx.com:8443/ws/v5/public',  # 备用WebSocket
                'priority': 2,
                'reconnect_delay': 5,
                'max_reconnect_attempts': 8,
                'heartbeat_timeout': 35
            },
            'bybit': {
                'name': 'Bybit',
                'websocket': 'wss://stream.bybit.com/v5/public/linear',
                'rest_api': 'https://api.bybit.com/v5/',
                'backup_ws': 'wss://stream.bybit.com/v5/public/linear',  # 备用WebSocket
                'priority': 3,
                'reconnect_delay': 7,
                'max_reconnect_attempts': 6,
                'heartbeat_timeout': 40
            }
        }
        
        # 初始化市场数据结构和连接状态
        for symbol in self.symbols:
            self.market_data[symbol] = {}
            self.last_update_time[symbol] = {}
            self.reconnect_attempts[symbol] = {}
            self.heartbeat_times[symbol] = {}
            self.connection_logs[symbol] = {}
            for exchange_id in self.exchanges_config.keys():
                self.last_update_time[symbol][exchange_id] = 0
                self.reconnect_attempts[symbol][exchange_id] = 0
                self.heartbeat_times[symbol][exchange_id] = 0
                self.connection_logs[symbol][exchange_id] = []
                self.connection_status[f"{symbol}_{exchange_id}"] = "disconnected"
    
    async def start_all_connections(self):
        """启动所有交易所连接"""
        # 启动真实的交易所连接
        asyncio.create_task(self.connect_to_exchanges())
        # 启动心跳检测任务
        asyncio.create_task(self.heartbeat_monitor())
        # 同时启动模拟数据作为备用
        asyncio.create_task(self.simulate_market_data())
    
    async def heartbeat_monitor(self):
        """心跳监控任务"""
        while True:
            try:
                current_time = time.time()
                for symbol in self.symbols:
                    for exchange_id in self.exchanges_config.keys():
                        # 检查连接状态
                        status_key = f"{symbol}_{exchange_id}"
                        current_status = self.connection_status.get(status_key)
                        
                        if current_status == "connected":
                            # 检查心跳超时
                            last_heartbeat = self.heartbeat_times[symbol][exchange_id]
                            heartbeat_timeout = self.exchanges_config[exchange_id].get('heartbeat_timeout', 30)
                            
                            time_since_heartbeat = current_time - last_heartbeat
                            if time_since_heartbeat > heartbeat_timeout:
                                logging.warning(f"交易所 {exchange_id} {symbol} 心跳超时 ({time_since_heartbeat:.1f}s > {heartbeat_timeout}s)，准备重连")
                                self.update_connection_status(symbol, exchange_id, "disconnected", f"心跳超时 {time_since_heartbeat:.1f}s")
                                # 触发重连
                                asyncio.create_task(self.reconnect_exchange(symbol, exchange_id))
                        elif current_status == "disconnected":
                            # 记录断开连接的持续时间
                            last_update = self.last_update_time[symbol][exchange_id]
                            time_since_disconnect = current_time - last_update
                            if time_since_disconnect > 60:  # 超过1分钟记录一次
                                logging.info(f"交易所 {exchange_id} {symbol} 已断开 {time_since_disconnect:.1f}s")
                
                await asyncio.sleep(10)  # 每10秒检查一次心跳
            except Exception as e:
                logging.error(f"Heartbeat monitor error: {e}")
                await asyncio.sleep(5)
    
    async def connect_to_exchanges(self):
        """连接到各个交易所"""
        # 这里应该实现真实的交易所连接逻辑
        # 由于这是一个演示系统，我们仍然使用模拟数据
        # 但在生产环境中，这里会包含真实的WebSocket连接代码
        pass
    
    async def reconnect_exchange(self, symbol: str, exchange_id: str):
        """重新连接指定的交易所"""
        try:
            # 增加重连尝试次数
            self.reconnect_attempts[symbol][exchange_id] += 1
            max_attempts = self.exchanges_config[exchange_id].get('max_reconnect_attempts', 5)
            
            if self.reconnect_attempts[symbol][exchange_id] > max_attempts:
                logging.error(f"交易所 {exchange_id} {symbol} 重连尝试次数超过限制 ({max_attempts})")
                self.update_connection_status(symbol, exchange_id, "failed")
                return
            
            # 获取重连延迟
            reconnect_delay = self.exchanges_config[exchange_id].get('reconnect_delay', 5)
            logging.info(f"准备重连交易所 {exchange_id} {symbol}，第 {self.reconnect_attempts[symbol][exchange_id]} 次尝试，{reconnect_delay} 秒后重连")
            
            # 等待重连延迟
            await asyncio.sleep(reconnect_delay)
            
            # 尝试重连（这里使用模拟重连）
            # 在实际实现中，这里会重新建立WebSocket连接
            logging.info(f"交易所 {exchange_id} {symbol} 重连成功")
            self.update_connection_status(symbol, exchange_id, "connected")
            self.reconnect_attempts[symbol][exchange_id] = 0  # 重置重连次数
            
        except Exception as e:
            logging.error(f"重连交易所 {exchange_id} {symbol} 失败: {e}")
            # 检查是否需要使用备用连接
            if self.reconnect_attempts[symbol][exchange_id] <= max_attempts:
                logging.info(f"尝试使用备用连接重连交易所 {exchange_id} {symbol}")
                asyncio.create_task(self.reconnect_exchange(symbol, exchange_id))
    
    def update_connection_status(self, symbol: str, exchange: str, status: str, message: str = ""):
        """更新连接状态"""
        key = f"{symbol}_{exchange}"
        old_status = self.connection_status.get(key, "unknown")
        self.connection_status[key] = status
        
        # 记录日志
        timestamp = int(time.time())
        log_entry = {
            "timestamp": timestamp,
            "from": old_status,
            "to": status,
            "message": message
        }
        
        # 限制日志数量，只保留最近100条
        if len(self.connection_logs[symbol][exchange]) >= 100:
            self.connection_logs[symbol][exchange].pop(0)
        self.connection_logs[symbol][exchange].append(log_entry)
        
        logging.info(f"连接状态更新: {key} -> {status} ({message})")
        
        # 如果连接成功，更新最后更新时间和心跳时间
        if status == "connected":
            current_time = time.time()
            self.last_update_time[symbol][exchange] = current_time
            self.heartbeat_times[symbol][exchange] = current_time
            self.reconnect_attempts[symbol][exchange] = 0  # 重置重连次数
    
    def update_heartbeat(self, symbol: str, exchange: str):
        """更新心跳时间"""
        if self.connection_status.get(f"{symbol}_{exchange}") == "connected":
            self.heartbeat_times[symbol][exchange] = time.time()
    
    async def simulate_market_data(self):
        """模拟市场数据（用于演示）"""
        base_prices = {'BTCUSDT': 43250.0, 'ETHUSDT': 2580.0}
        
        while True:
            try:
                for symbol in self.symbols:
                    base_price = base_prices[symbol]
                    
                    for exchange_id, config in self.exchanges_config.items():
                        # 生成模拟数据
                        price_variation = random.uniform(-0.02, 0.02)  # ±2%变化
                        current_price = base_price * (1 + price_variation)
                        
                        market_data = MarketData()
                        market_data.symbol = symbol
                        market_data.exchange = exchange_id
                        market_data.price = current_price
                        market_data.volume_24h = random.uniform(10000, 50000)
                        market_data.change_percent_24h = random.uniform(-5, 5)
                        market_data.high_24h = current_price * 1.05
                        market_data.low_24h = current_price * 0.95
                        market_data.funding_rate = random.uniform(-0.001, 0.001)
                        market_data.open_interest = random.uniform(100000, 500000)
                        market_data.timestamp = int(time.time() * 1000)
                        
                        # 存储数据
                        self.market_data[symbol][exchange_id] = market_data
                        
                        # 更新基础价格（模拟价格波动）
                        base_prices[symbol] = current_price
                
                await asyncio.sleep(2)  # 每2秒更新一次
                
            except Exception as e:
                logging.error(f"Simulate market data error: {e}")
                await asyncio.sleep(5)
    
    def get_latest_market_data(self) -> Dict:
        """获取最新市场数据"""
        result = {}
        for symbol, exchanges in self.market_data.items():
            result[symbol] = {}
            for exchange, data in exchanges.items():
                result[symbol][exchange] = data.to_dict()
        return result
    
    def get_symbol_data(self, symbol: str) -> Dict:
        """获取指定交易对数据"""
        return {
            exchange: data.to_dict() 
            for exchange, data in self.market_data.get(symbol, {}).items()
        }
    
    def get_aggregated_data(self, symbol: str) -> Dict:
        """获取聚合数据"""
        exchanges_data = self.market_data.get(symbol, {})
        if not exchanges_data:
            return {}
        
        prices = [data.price for data in exchanges_data.values()]
        volumes = [data.volume_24h for data in exchanges_data.values()]
        
        if not prices:
            return {}
        
        return {
            'symbol': symbol,
            'avg_price': sum(prices) / len(prices),
            'max_price': max(prices),
            'min_price': min(prices),
            'price_spread': max(prices) - min(prices),
            'total_volume': sum(volumes),
            'exchange_count': len(prices),
            'timestamp': int(time.time())
        }

class BinanceHandler:
    """币安交易所数据处理器"""
    
    def get_websocket_url(self, symbols: List[str]) -> str:
        streams = []
        for symbol in symbols:
            symbol_lower = symbol.lower()
            streams.extend([
                f"{symbol_lower}@ticker",
                f"{symbol_lower}@depth20@100ms"
            ])
        return f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"
    
    def parse_market_data(self, data: dict) -> Optional[MarketData]:
        if 'data' not in data:
            return None
            
        stream_data = data['data']
        stream_name = data.get('stream', '')
        
        if '@ticker' in stream_name:
            market_data = MarketData()
            market_data.exchange = 'binance'
            market_data.symbol = stream_data['s']
            market_data.price = float(stream_data['c'])
            market_data.volume_24h = float(stream_data['v'])
            market_data.change_percent_24h = float(stream_data['P'])
            market_data.high_24h = float(stream_data['h'])
            market_data.low_24h = float(stream_data['l'])
            market_data.timestamp = int(stream_data['E'])
            
            return market_data
        
        return None

class OKXHandler:
    """OKX交易所数据处理器"""
    
    def get_websocket_url(self, symbols: List[str]) -> str:
        return "wss://ws.okx.com:8443/ws/v5/public"
    
    def get_subscribe_message(self, symbols: List[str]) -> dict:
        args = []
        for symbol in symbols:
            args.append({
                "channel": "tickers",
                "instId": symbol
            })
        
        return {
            "op": "subscribe",
            "args": args
        }
    
    def parse_market_data(self, data: dict) -> Optional[MarketData]:
        if 'data' not in data:
            return None
        
        for item in data['data']:
            market_data = MarketData()
            market_data.exchange = 'okx'
            market_data.symbol = item['instId']
            market_data.price = float(item['last'])
            market_data.volume_24h = float(item['vol24h'])
            market_data.change_percent_24h = float(item['chgUtc']) * 100
            market_data.high_24h = float(item['high24h'])
            market_data.low_24h = float(item['low24h'])
            market_data.timestamp = int(item['ts'])
            
            return market_data
        
        return None
