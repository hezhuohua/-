"""
AI增强型交易策略服务
结合传统技术指标和AI模型，提供智能化的交易信号
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass
import json

@dataclass
class StrategySignal:
    """策略信号数据类"""
    signal_type: str  # 'buy', 'sell', 'hold'
    confidence: float  # 0-1 置信度
    price: float  # 当前价格
    timestamp: datetime  # 信号时间
    strategy_name: str  # 策略名称
    ai_enhancement: Dict  # AI增强信息
    explanation: str  # 策略解释
    risk_level: str  # 风险等级

@dataclass
class MarketData:
    """市场数据结构"""
    prices: List[float]
    volumes: List[float]
    timestamps: List[datetime]
    symbol: str

class AIStrategyService:
    """AI增强型交易策略服务"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.strategies = {
            'ma_cross': self.ma_cross_strategy,
            'momentum_reversal': self.momentum_reversal_strategy,
            'ai_enhanced_ma': self.ai_enhanced_ma_strategy,
            'ai_enhanced_momentum': self.ai_enhanced_momentum_strategy
        }

    def calculate_technical_indicators(self, market_data: MarketData) -> Dict:
        """计算技术指标"""
        try:
            prices = np.array(market_data.prices)

            # 计算移动平均线
            ma5 = self._calculate_ma(prices, 5)
            ma10 = self._calculate_ma(prices, 10)
            ma20 = self._calculate_ma(prices, 20)
            ma50 = self._calculate_ma(prices, 50)

            # 计算RSI
            rsi = self._calculate_rsi(prices, 14)

            # 计算布林带
            bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(prices, 20, 2)

            # 计算MACD
            macd, signal, histogram = self._calculate_macd(prices)

            # 计算成交量指标
            volume_ma = self._calculate_ma(market_data.volumes, 20)
            volume_ratio = market_data.volumes[-1] / volume_ma[-1] if volume_ma[-1] > 0 else 1

            return {
                'ma5': ma5,
                'ma10': ma10,
                'ma20': ma20,
                'ma50': ma50,
                'rsi': rsi,
                'bollinger_bands': {
                    'upper': bb_upper,
                    'middle': bb_middle,
                    'lower': bb_lower
                },
                'macd': {
                    'macd': macd,
                    'signal': signal,
                    'histogram': histogram
                },
                'volume_ratio': volume_ratio,
                'current_price': prices[-1],
                'price_change': ((prices[-1] - prices[-2]) / prices[-2] * 100) if len(prices) > 1 else 0
            }
        except Exception as e:
            self.logger.error(f"计算技术指标失败: {e}")
            return {}

    def _calculate_ma(self, prices: np.ndarray, period: int) -> np.ndarray:
        """计算移动平均线"""
        return np.convolve(prices, np.ones(period)/period, mode='valid')

    def _calculate_rsi(self, prices: np.ndarray, period: int = 14) -> np.ndarray:
        """计算RSI指标"""
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gains = np.convolve(gains, np.ones(period)/period, mode='valid')
        avg_losses = np.convolve(losses, np.ones(period)/period, mode='valid')

        rs = avg_gains / (avg_losses + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calculate_bollinger_bands(self, prices: np.ndarray, period: int = 20, std_dev: float = 2) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """计算布林带"""
        ma = self._calculate_ma(prices, period)
        std = np.array([np.std(prices[i:i+period]) for i in range(len(prices)-period+1)])

        upper = ma + (std * std_dev)
        lower = ma - (std * std_dev)

        return upper, ma, lower

    def _calculate_macd(self, prices: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """计算MACD指标"""
        ema_fast = self._calculate_ema(prices, fast)
        ema_slow = self._calculate_ema(prices, slow)

        macd_line = ema_fast - ema_slow
        signal_line = self._calculate_ema(macd_line, signal)
        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    def _calculate_ema(self, prices: np.ndarray, period: int) -> np.ndarray:
        """计算指数移动平均线"""
        alpha = 2 / (period + 1)
        ema = np.zeros_like(prices)
        ema[0] = prices[0]

        for i in range(1, len(prices)):
            ema[i] = alpha * prices[i] + (1 - alpha) * ema[i-1]

        return ema

    def ma_cross_strategy(self, market_data: MarketData, params: Dict = None) -> StrategySignal:
        """传统均线交叉策略"""
        if params is None:
            params = {'short_period': 5, 'long_period': 20}

        indicators = self.calculate_technical_indicators(market_data)
        if not indicators:
            return self._create_hold_signal("技术指标计算失败")

        short_ma = indicators[f'ma{params["short_period"]}']
        long_ma = indicators[f'ma{params["long_period"]}']

        if len(short_ma) < 2 or len(long_ma) < 2:
            return self._create_hold_signal("数据不足")

        current_short = short_ma[-1]
        current_long = long_ma[-1]
        prev_short = short_ma[-2]
        prev_long = long_ma[-2]

        # 判断交叉信号
        if current_short > current_long and prev_short <= prev_long:
            # 金叉 - 买入信号
            confidence = min(0.8, abs(current_short - current_long) / current_long * 10)
            return StrategySignal(
                signal_type='buy',
                confidence=confidence,
                price=indicators['current_price'],
                timestamp=datetime.now(),
                strategy_name='均线交叉策略',
                ai_enhancement={},
                explanation=f"短期均线({params['short_period']}日)上穿长期均线({params['long_period']}日)，产生买入信号",
                risk_level='medium'
            )
        elif current_short < current_long and prev_short >= prev_long:
            # 死叉 - 卖出信号
            confidence = min(0.8, abs(current_short - current_long) / current_long * 10)
            return StrategySignal(
                signal_type='sell',
                confidence=confidence,
                price=indicators['current_price'],
                timestamp=datetime.now(),
                strategy_name='均线交叉策略',
                ai_enhancement={},
                explanation=f"短期均线({params['short_period']}日)下穿长期均线({params['long_period']}日)，产生卖出信号",
                risk_level='medium'
            )
        else:
            return self._create_hold_signal("均线未发生交叉")

    def momentum_reversal_strategy(self, market_data: MarketData, params: Dict = None) -> StrategySignal:
        """动量反转策略"""
        if params is None:
            params = {'oversold_rsi': 30, 'oversold_threshold': -10}

        indicators = self.calculate_technical_indicators(market_data)
        if not indicators:
            return self._create_hold_signal("技术指标计算失败")

        current_price = indicators['current_price']
        price_change = indicators['price_change']
        rsi = indicators['rsi']
        volume_ratio = indicators['volume_ratio']

        if len(rsi) == 0:
            return self._create_hold_signal("RSI数据不足")

        current_rsi = rsi[-1]

        # 判断超卖条件
        is_oversold = (price_change < params['oversold_threshold'] and
                      current_rsi < params['oversold_rsi'])

        if is_oversold:
            # 计算反弹概率
            bounce_probability = self._calculate_bounce_probability(
                price_change, current_rsi, volume_ratio
            )

            if bounce_probability > 0.6:
                return StrategySignal(
                    signal_type='buy',
                    confidence=bounce_probability,
                    price=current_price,
                    timestamp=datetime.now(),
                    strategy_name='动量反转策略',
                    ai_enhancement={
                        'bounce_probability': bounce_probability,
                        'oversold_level': 'high' if current_rsi < 20 else 'medium'
                    },
                    explanation=f"价格下跌{abs(price_change):.1f}%，RSI为{current_rsi:.1f}，处于超卖区域，反弹概率{bounce_probability:.1%}",
                    risk_level='high'
                )

        return self._create_hold_signal("未满足反转条件")

    def ai_enhanced_ma_strategy(self, market_data: MarketData, params: Dict = None,
                               ai_context: Dict = None) -> StrategySignal:
        """AI增强型均线交叉策略"""
        # 获取基础信号
        base_signal = self.ma_cross_strategy(market_data, params)

        if base_signal.signal_type == 'hold':
            return base_signal

        # AI增强分析
        ai_enhancement = self._analyze_market_context(market_data, ai_context)

        # 根据AI分析调整信号
        adjusted_signal = self._adjust_signal_with_ai(base_signal, ai_enhancement)

        return adjusted_signal

    def ai_enhanced_momentum_strategy(self, market_data: MarketData, params: Dict = None,
                                    ai_context: Dict = None) -> StrategySignal:
        """AI增强型动量反转策略"""
        # 获取基础信号
        base_signal = self.momentum_reversal_strategy(market_data, params)

        if base_signal.signal_type == 'hold':
            return base_signal

        # AI增强分析
        ai_enhancement = self._analyze_market_context(market_data, ai_context)

        # 根据AI分析调整信号
        adjusted_signal = self._adjust_signal_with_ai(base_signal, ai_enhancement)

        return adjusted_signal

    def _analyze_market_context(self, market_data: MarketData, ai_context: Dict = None) -> Dict:
        """AI市场环境分析"""
        if ai_context is None:
            ai_context = {}

        indicators = self.calculate_technical_indicators(market_data)

        # 市场情绪分析
        market_sentiment = self._analyze_market_sentiment(indicators, ai_context)

        # 风险分析
        risk_analysis = self._analyze_risk_factors(indicators, ai_context)

        # 趋势强度分析
        trend_strength = self._analyze_trend_strength(indicators)

        return {
            'market_sentiment': market_sentiment,
            'risk_analysis': risk_analysis,
            'trend_strength': trend_strength,
            'ai_recommendation': self._generate_ai_recommendation(
                market_sentiment, risk_analysis, trend_strength
            )
        }

    def _analyze_market_sentiment(self, indicators: Dict, ai_context: Dict) -> Dict:
        """分析市场情绪"""
        # 基于技术指标的情绪分析
        rsi_sentiment = 'bullish' if indicators.get('rsi', [50])[-1] > 50 else 'bearish'
        volume_sentiment = 'high' if indicators.get('volume_ratio', 1) > 1.5 else 'normal'

        # 价格动量情绪
        price_change = indicators.get('price_change', 0)
        momentum_sentiment = 'bullish' if price_change > 2 else 'bearish' if price_change < -2 else 'neutral'

        # 综合情绪评分
        sentiment_score = 0
        if rsi_sentiment == 'bullish': sentiment_score += 1
        if volume_sentiment == 'high': sentiment_score += 1
        if momentum_sentiment == 'bullish': sentiment_score += 1

        overall_sentiment = 'bullish' if sentiment_score >= 2 else 'bearish' if sentiment_score <= 0 else 'neutral'

        return {
            'overall': overall_sentiment,
            'rsi': rsi_sentiment,
            'volume': volume_sentiment,
            'momentum': momentum_sentiment,
            'score': sentiment_score
        }

    def _analyze_risk_factors(self, indicators: Dict, ai_context: Dict) -> Dict:
        """分析风险因素"""
        risk_factors = []
        risk_level = 'low'

        # RSI极端值风险
        if indicators.get('rsi'):
            current_rsi = indicators['rsi'][-1]
            if current_rsi > 80 or current_rsi < 20:
                risk_factors.append('RSI极端值')
                risk_level = 'high'

        # 价格波动风险
        price_change = abs(indicators.get('price_change', 0))
        if price_change > 15:
            risk_factors.append('价格剧烈波动')
            risk_level = 'high'
        elif price_change > 8:
            risk_factors.append('价格较大波动')
            risk_level = 'medium'

        # 成交量异常风险
        volume_ratio = indicators.get('volume_ratio', 1)
        if volume_ratio > 3:
            risk_factors.append('成交量异常放大')
            risk_level = 'medium'

        return {
            'level': risk_level,
            'factors': risk_factors,
            'price_volatility': price_change,
            'volume_anomaly': volume_ratio
        }

    def _analyze_trend_strength(self, indicators: Dict) -> Dict:
        """分析趋势强度"""
        # 均线排列分析
        ma5 = indicators.get('ma5', [])
        ma20 = indicators.get('ma20', [])
        ma50 = indicators.get('ma50', [])

        if len(ma5) == 0 or len(ma20) == 0 or len(ma50) == 0:
            return {'strength': 'unknown', 'direction': 'unknown'}

        # 均线排列
        current_ma5 = ma5[-1]
        current_ma20 = ma20[-1]
        current_ma50 = ma50[-1]

        # 判断趋势方向和强度
        if current_ma5 > current_ma20 > current_ma50:
            trend_direction = 'uptrend'
            trend_strength = 'strong' if (current_ma5 - current_ma50) / current_ma50 > 0.1 else 'moderate'
        elif current_ma5 < current_ma20 < current_ma50:
            trend_direction = 'downtrend'
            trend_strength = 'strong' if (current_ma50 - current_ma5) / current_ma50 > 0.1 else 'moderate'
        else:
            trend_direction = 'sideways'
            trend_strength = 'weak'

        return {
            'strength': trend_strength,
            'direction': trend_direction,
            'ma_alignment': f"MA5: {current_ma5:.2f}, MA20: {current_ma20:.2f}, MA50: {current_ma50:.2f}"
        }

    def _generate_ai_recommendation(self, sentiment: Dict, risk: Dict, trend: Dict) -> str:
        """生成AI建议"""
        recommendations = []

        # 基于情绪的推荐
        if sentiment['overall'] == 'bullish':
            recommendations.append("市场情绪偏乐观，有利于多头策略")
        elif sentiment['overall'] == 'bearish':
            recommendations.append("市场情绪偏悲观，有利于空头策略")

        # 基于风险的推荐
        if risk['level'] == 'high':
            recommendations.append("⚠️ 风险等级较高，建议降低仓位或设置严格止损")
        elif risk['level'] == 'medium':
            recommendations.append("⚠️ 风险等级中等，建议谨慎操作")
        else:
            recommendations.append("✅ 风险等级较低，可适当增加仓位")

        # 基于趋势的推荐
        if trend['strength'] == 'strong':
            recommendations.append(f"趋势强度较强，建议顺势而为")
        elif trend['strength'] == 'moderate':
            recommendations.append(f"趋势强度中等，可适度参与")
        else:
            recommendations.append("趋势不明显，建议观望或短线操作")

        return " | ".join(recommendations)

    def _adjust_signal_with_ai(self, base_signal: StrategySignal, ai_enhancement: Dict) -> StrategySignal:
        """根据AI分析调整信号"""
        # 复制基础信号
        adjusted_signal = StrategySignal(
            signal_type=base_signal.signal_type,
            confidence=base_signal.confidence,
            price=base_signal.price,
            timestamp=base_signal.timestamp,
            strategy_name=base_signal.strategy_name + " (AI增强)",
            ai_enhancement=ai_enhancement,
            explanation=base_signal.explanation,
            risk_level=base_signal.risk_level
        )

        # 根据AI分析调整置信度
        sentiment_score = ai_enhancement.get('market_sentiment', {}).get('score', 1)
        risk_level = ai_enhancement.get('risk_analysis', {}).get('level', 'medium')
        trend_strength = ai_enhancement.get('trend_strength', {}).get('strength', 'moderate')

        # 调整置信度
        confidence_adjustment = 0

        # 情绪调整
        if base_signal.signal_type == 'buy' and sentiment_score >= 2:
            confidence_adjustment += 0.1
        elif base_signal.signal_type == 'sell' and sentiment_score <= 0:
            confidence_adjustment += 0.1

        # 风险调整
        if risk_level == 'high':
            confidence_adjustment -= 0.2
        elif risk_level == 'low':
            confidence_adjustment += 0.1

        # 趋势调整
        if trend_strength == 'strong':
            confidence_adjustment += 0.15
        elif trend_strength == 'weak':
            confidence_adjustment -= 0.1

        # 应用调整
        adjusted_signal.confidence = max(0.1, min(0.95, base_signal.confidence + confidence_adjustment))

        # 更新解释
        ai_recommendation = ai_enhancement.get('ai_recommendation', '')
        adjusted_signal.explanation += f"\n\n🤖 AI分析: {ai_recommendation}"

        # 更新风险等级
        if risk_level == 'high':
            adjusted_signal.risk_level = 'high'
        elif risk_level == 'medium' and adjusted_signal.risk_level == 'low':
            adjusted_signal.risk_level = 'medium'

        return adjusted_signal

    def _calculate_bounce_probability(self, price_change: float, rsi: float, volume_ratio: float) -> float:
        """计算反弹概率"""
        # 基于价格跌幅的反弹概率
        price_factor = min(1.0, abs(price_change) / 20.0)  # 最大20%跌幅

        # 基于RSI的反弹概率
        rsi_factor = 1.0
        if rsi < 20:
            rsi_factor = 0.9
        elif rsi < 30:
            rsi_factor = 0.7
        elif rsi < 40:
            rsi_factor = 0.5

        # 基于成交量的反弹概率
        volume_factor = min(1.0, volume_ratio / 2.0)  # 成交量放大2倍以上

        # 综合计算
        probability = (price_factor * 0.4 + rsi_factor * 0.4 + volume_factor * 0.2)

        return min(0.95, probability)

    def _create_hold_signal(self, reason: str) -> StrategySignal:
        """创建观望信号"""
        return StrategySignal(
            signal_type='hold',
            confidence=0.0,
            price=0.0,
            timestamp=datetime.now(),
            strategy_name='策略分析',
            ai_enhancement={},
            explanation=reason,
            risk_level='low'
        )

    def get_available_strategies(self) -> List[Dict]:
        """获取可用策略列表"""
        return [
            {
                'id': 'ma_cross',
                'name': '均线交叉策略',
                'description': '基于短期和长期均线交叉的传统策略',
                'category': 'trend_following',
                'complexity': 'low',
                'risk_level': 'medium'
            },
            {
                'id': 'momentum_reversal',
                'name': '动量反转策略',
                'description': '捕捉超跌反弹机会的反转策略',
                'category': 'mean_reversion',
                'complexity': 'medium',
                'risk_level': 'high'
            },
            {
                'id': 'ai_enhanced_ma',
                'name': 'AI增强均线策略',
                'description': '结合AI市场分析的智能均线策略',
                'category': 'ai_enhanced',
                'complexity': 'medium',
                'risk_level': 'medium'
            },
            {
                'id': 'ai_enhanced_momentum',
                'name': 'AI增强动量策略',
                'description': 'AI辅助的超跌反弹策略',
                'category': 'ai_enhanced',
                'complexity': 'high',
                'risk_level': 'high'
            }
        ]

    def run_strategy(self, strategy_id: str, market_data: MarketData,
                    params: Dict = None, ai_context: Dict = None) -> StrategySignal:
        """运行指定策略"""
        if strategy_id not in self.strategies:
            raise ValueError(f"未知策略: {strategy_id}")

        strategy_func = self.strategies[strategy_id]

        if strategy_id.startswith('ai_enhanced'):
            return strategy_func(market_data, params, ai_context)
        else:
            return strategy_func(market_data, params)
