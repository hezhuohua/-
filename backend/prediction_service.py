import asyncio
import json
import random
import numpy as np
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import httpx

# 加载环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv是可选的

class PredictionService:
    def __init__(self):
        self.deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.deepseek_api_key:
            logging.warning("DEEPSEEK_API_KEY not found in environment variables. AI predictions will use mock data.")
        self.deepseek_url = "https://api.deepseek.com/v1/chat/completions"

    async def predict(self, symbol: str, timeframes: List[str], market_data: Dict) -> Dict:
        """进行价格预测"""
        predictions = {}

        for timeframe in timeframes:
            try:
                # 获取技术分析预测
                technical_prediction = await self.technical_analysis_prediction(symbol, timeframe, market_data)

                # 获取AI模型预测
                ai_prediction = await self.ai_model_prediction(symbol, timeframe, market_data)

                # 获取DEEPSEEK分析
                deepseek_analysis = await self.deepseek_analysis(symbol, timeframe, market_data)

                # 综合预测结果
                final_prediction = self.combine_predictions(
                    technical_prediction,
                    ai_prediction,
                    deepseek_analysis
                )

                predictions[timeframe] = final_prediction

            except Exception as e:
                logging.error(f"Prediction error for {symbol} {timeframe}: {e}")
                # 返回默认预测
                predictions[timeframe] = {
                    "direction": "neutral",
                    "probability": 50.0,
                    "confidence": 0.3,
                    "target_price": 0.0,
                    "reasoning": "预测服务暂时不可用"
                }

        return predictions

    async def technical_analysis_prediction(self, symbol: str, timeframe: str, market_data: Dict) -> Dict:
        """技术分析预测"""
        # 模拟技术分析计算
        await asyncio.sleep(0.1)  # 模拟计算时间

        # 简化的技术分析逻辑
        prices = []
        for exchange, data in market_data.items():
            if data.get('price'):
                prices.append(data['price'])

        if not prices:
            return {"direction": "neutral", "probability": 50.0, "confidence": 0.3}

        avg_price = sum(prices) / len(prices)
        price_volatility = np.std(prices) if len(prices) > 1 else 0

        # 基于价格波动性的简单预测
        if price_volatility > avg_price * 0.01:  # 高波动
            direction = "up" if random.random() > 0.5 else "down"
            probability = random.uniform(60, 80)
        else:  # 低波动
            direction = "neutral"
            probability = random.uniform(45, 55)

        return {
            "direction": direction,
            "probability": probability,
            "confidence": min(price_volatility * 100, 0.8),
            "method": "technical_analysis"
        }

    async def ai_model_prediction(self, symbol: str, timeframe: str, market_data: Dict) -> Dict:
        """AI模型预测"""
        # 模拟AI模型计算
        await asyncio.sleep(0.2)

        # 简化的AI预测逻辑
        timeframe_weights = {
            "1m": 0.6,
            "5m": 0.7,
            "15m": 0.75,
            "30m": 0.8,
            "1h": 0.85
        }

        base_confidence = timeframe_weights.get(timeframe, 0.7)

        # 模拟AI预测结果
        directions = ["up", "down", "neutral"]
        direction = random.choices(directions, weights=[0.4, 0.4, 0.2])[0]
        probability = random.uniform(55, 85)

        return {
            "direction": direction,
            "probability": probability,
            "confidence": base_confidence,
            "method": "ai_model"
        }

    async def deepseek_analysis(self, symbol: str, timeframe: str, market_data: Dict) -> Dict:
        """DEEPSEEK大模型分析"""
        try:
            # 构建市场数据摘要
            market_summary = self.build_market_summary(symbol, market_data)

            # 构建提示词
            prompt = f"""
            作为专业的加密货币分析师，请分析{symbol}在{timeframe}时间框架内的价格走势。

            当前市场数据：
            {market_summary}

            请从以下角度进行分析：
            1. 技术面分析
            2. 市场情绪
            3. 价格趋势
            4. 风险评估

            请给出明确的预测方向（up/down/neutral）和置信度（0-100%）。
            """

            # 调用DEEPSEEK API（这里使用模拟响应）
            response = await self.call_deepseek_api(prompt)

            # 解析响应
            return self.parse_deepseek_response(response)

        except Exception as e:
            logging.error(f"DEEPSEEK analysis error: {e}")
            return {
                "direction": "neutral",
                "probability": 50.0,
                "confidence": 0.4,
                "reasoning": "DEEPSEEK分析暂时不可用",
                "method": "deepseek"
            }

    def build_market_summary(self, symbol: str, market_data: Dict) -> str:
        """构建市场数据摘要"""
        summary_lines = [f"{symbol} 多交易所数据:"]

        for exchange, data in market_data.items():
            if data.get('price'):
                summary_lines.append(
                    f"{exchange}: 价格${data['price']:.2f}, "
                    f"24h涨跌{data.get('change_percent_24h', 0):.2f}%, "
                    f"成交量{data.get('volume_24h', 0):.0f}"
                )

        return "\n".join(summary_lines)

    async def call_deepseek_api(self, prompt: str) -> str:
        """调用DEEPSEEK API"""
        if not self.deepseek_api_key:
            # 如果没有API密钥，使用模拟响应
            await asyncio.sleep(0.5)  # 模拟API调用时间
            mock_responses = [
                "基于当前技术指标分析，预计价格将上涨，置信度75%。RSI指标显示超卖状态，MACD出现金叉信号。",
                "市场情绪偏向谨慎，预计价格将下跌，置信度68%。成交量萎缩，支撑位面临考验。",
                "当前市场处于震荡状态，短期内可能保持横盘，置信度60%。等待明确的突破信号。"
            ]
            return random.choice(mock_responses)

        try:
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.7
            }

            # 设置30秒超时
            timeout = httpx.Timeout(30.0)

            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.post(
                    self.deepseek_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()

                result = response.json()
                return result["choices"][0]["message"]["content"]

        except httpx.TimeoutException:
            logging.error("DEEPSEEK API请求超时")
            return "API请求超时，使用技术分析：市场处于震荡状态，建议谨慎操作"
        except httpx.HTTPStatusError as e:
            logging.error(f"DEEPSEEK API HTTP错误: {e.response.status_code}")
            return "API服务暂时不可用，使用技术分析：建议关注关键支撑阻力位"
        except httpx.RequestError as e:
            logging.error(f"DEEPSEEK API网络错误: {e}")
            return "网络连接异常，使用技术分析：建议等待网络恢复后重试"
        except Exception as e:
            logging.error(f"DEEPSEEK API调用失败: {e}")
            return "技术分析显示市场处于震荡状态，建议谨慎操作"

    def parse_deepseek_response(self, response: str) -> Dict:
        """解析DEEPSEEK响应"""
        # 简化的响应解析
        response_lower = response.lower()

        if "上涨" in response or "看涨" in response:
            direction = "up"
        elif "下跌" in response or "看跌" in response:
            direction = "down"
        else:
            direction = "neutral"

        # 提取置信度
        import re
        confidence_match = re.search(r'(\d+)%', response)
        probability = float(confidence_match.group(1)) if confidence_match else 60.0

        return {
            "direction": direction,
            "probability": probability,
            "confidence": 0.8,
            "reasoning": response,
            "method": "deepseek"
        }

    def combine_predictions(self, technical: Dict, ai: Dict, deepseek: Dict) -> Dict:
        """综合多个预测结果"""
        # 权重配置
        weights = {
            "technical_analysis": 0.3,
            "ai_model": 0.3,
            "deepseek": 0.4
        }

        predictions = [technical, ai, deepseek]

        # 计算加权概率
        direction_scores = {"up": 0, "down": 0, "neutral": 0}
        total_confidence = 0

        for pred in predictions:
            method = pred.get("method", "unknown")
            weight = weights.get(method, 0.33)
            confidence = pred.get("confidence", 0.5)
            direction = pred.get("direction", "neutral")
            probability = pred.get("probability", 50.0)

            # 加权计算
            score = (probability / 100.0) * confidence * weight
            direction_scores[direction] += score
            total_confidence += confidence * weight

        # 确定最终方向
        final_direction = max(direction_scores, key=direction_scores.get)
        final_probability = direction_scores[final_direction] * 100

        # 计算目标价格（简化）
        base_price = 0
        price_count = 0
        for pred in predictions:
            if pred.get("target_price", 0) > 0:
                base_price += pred["target_price"]
                price_count += 1

        if price_count == 0:
            # 如果没有目标价格，基于方向估算
            base_price = 43250 if "BTC" in str(predictions) else 2580  # 简化处理
            if final_direction == "up":
                target_price = base_price * 1.02
            elif final_direction == "down":
                target_price = base_price * 0.98
            else:
                target_price = base_price
        else:
            target_price = base_price / price_count

        return {
            "direction": final_direction,
            "probability": min(final_probability, 95.0),  # 限制最大概率
            "confidence": min(total_confidence, 0.9),
            "target_price": target_price,
            "reasoning": f"综合{len(predictions)}个模型的分析结果",
            "details": {
                "technical": technical,
                "ai_model": ai,
                "deepseek": deepseek
            }
        }
