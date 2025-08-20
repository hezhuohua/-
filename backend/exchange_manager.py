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
        
        # 交易所配置
        self.exchanges_config = {
            'binance': {
                'name': '币安',
                'websocket': 'wss://stream.binance.com:9443/ws/',
                'rest_api': 'https://api.binance.com/api/v3/',
                'priority': 1
            },
            'okx': {
                'name': 'OKX',
                'websocket': 'wss://ws.okx.com:8443/ws/v5/public',
                'rest_api': 'https://www.okx.com/api/v5/',
                'priority': 2
            },
            'bybit': {
                'name': 'Bybit',
                'websocket': 'wss://stream.bybit.com/v5/public/linear',
                'rest_api': 'https://api.bybit.com/v5/',
                'priority': 3
            }
        }
        
        # 初始化市场数据结构
        for symbol in self.symbols:
            self.market_data[symbol] = {}
    
    async def start_all_connections(self):
        """启动所有交易所连接"""
        # 为了演示，我们使用模拟数据
        asyncio.create_task(self.simulate_market_data())
    
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
