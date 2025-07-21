#!/usr/bin/env python3
"""
Hyperliquid Pump Chart Monitor
Fetches pump chart data every 10 minutes and provides technical analysis
"""

import requests
import json
import time
import websocket
import threading
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
from typing import Dict, List, Optional, Tuple
import signal
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hyperliquid_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class HyperliquidMonitor:
    def __init__(self, token_symbol: str = "PURR"):
        self.token_symbol = token_symbol
        self.base_url = "https://api.hyperliquid.xyz"
        self.ws_url = "wss://api.hyperliquid.xyz/ws"
        self.price_history = []
        self.volume_history = []
        self.trade_history = []
        self.candle_data = []
        self.ws = None
        self.running = False
        
        # Technical analysis parameters
        self.sma_periods = [9, 20, 50]
        self.ema_periods = [12, 26]
        self.rsi_period = 14
        self.bb_period = 20
        self.bb_std = 2
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info("Received shutdown signal. Stopping monitor...")
        self.running = False
        if self.ws:
            self.ws.close()
        sys.exit(0)
    
    def get_spot_metadata(self) -> Dict:
        """Get spot metadata to understand token info"""
        try:
            response = requests.post(
                f"{self.base_url}/info",
                json={"type": "spotMeta"},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching spot metadata: {e}")
            return {}
    
    def get_spot_asset_contexts(self) -> Dict:
        """Get current market data for all spot assets"""
        try:
            response = requests.post(
                f"{self.base_url}/info",
                json={"type": "spotMetaAndAssetCtxs"},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching spot asset contexts: {e}")
            return {}
    
    def get_candle_data(self, interval: str = "15m", num_candles: int = 100) -> List[Dict]:
        """Get historical candlestick data"""
        try:
            # Calculate start time for the requested number of candles
            interval_minutes = {
                "1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30, 
                "1h": 60, "2h": 120, "4h": 240, "8h": 480, "12h": 720, "1d": 1440
            }
            
            if interval not in interval_minutes:
                interval = "15m"
            
            minutes_back = interval_minutes[interval] * num_candles
            start_time = int((datetime.now() - timedelta(minutes=minutes_back)).timestamp() * 1000)
            
            response = requests.post(
                f"{self.base_url}/info",
                json={
                    "type": "candleSnapshot",
                    "req": {
                        "coin": self.token_symbol,
                        "interval": interval,
                        "startTime": start_time
                    }
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching candle data: {e}")
            return []
    
    def calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    def calculate_ema(self, prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return None
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return None
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, std_dev: float = 2) -> Tuple[float, float, float]:
        """Calculate Bollinger Bands (upper, middle, lower)"""
        if len(prices) < period:
            return None, None, None
        
        recent_prices = prices[-period:]
        sma = sum(recent_prices) / period
        
        variance = sum((price - sma) ** 2 for price in recent_prices) / period
        std = variance ** 0.5
        
        upper = sma + (std_dev * std)
        lower = sma - (std_dev * std)
        
        return upper, sma, lower
    
    def calculate_macd(self, prices: List[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Tuple[float, float, float]:
        """Calculate MACD (MACD line, Signal line, Histogram)"""
        if len(prices) < slow_period:
            return None, None, None
        
        ema_fast = self.calculate_ema(prices, fast_period)
        ema_slow = self.calculate_ema(prices, slow_period)
        
        if ema_fast is None or ema_slow is None:
            return None, None, None
        
        macd_line = ema_fast - ema_slow
        
        # For signal line, we need MACD history
        if len(self.price_history) < slow_period + signal_period:
            return macd_line, None, None
        
        macd_history = []
        for i in range(len(prices) - slow_period + 1):
            subset = prices[i:i + slow_period]
            fast_ema = self.calculate_ema(subset[-fast_period:], fast_period) if len(subset) >= fast_period else None
            slow_ema = self.calculate_ema(subset, slow_period)
            if fast_ema and slow_ema:
                macd_history.append(fast_ema - slow_ema)
        
        if len(macd_history) >= signal_period:
            signal_line = self.calculate_ema(macd_history, signal_period)
            histogram = macd_line - signal_line if signal_line else None
            return macd_line, signal_line, histogram
        
        return macd_line, None, None
    
    def analyze_market_data(self, current_price: float, volume: float) -> Dict:
        """Perform comprehensive technical analysis"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "token": self.token_symbol,
            "current_price": current_price,
            "volume": volume,
            "price_change_24h": None,
            "volume_change_24h": None,
            "trend_analysis": {},
            "momentum_indicators": {},
            "volatility_indicators": {},
            "support_resistance": {},
            "signals": []
        }
        
        if len(self.price_history) < 2:
            analysis["signals"].append("Insufficient data for analysis")
            return analysis
        
        # Price change analysis
        if len(self.price_history) >= 144:  # 24 hours of 10-minute intervals
            price_24h_ago = self.price_history[-144]
            analysis["price_change_24h"] = ((current_price - price_24h_ago) / price_24h_ago) * 100
        
        if len(self.volume_history) >= 144:
            volume_24h_ago = self.volume_history[-144]
            if volume_24h_ago > 0:
                analysis["volume_change_24h"] = ((volume - volume_24h_ago) / volume_24h_ago) * 100
        
        # Moving averages
        prices = self.price_history
        for period in self.sma_periods:
            sma = self.calculate_sma(prices, period)
            if sma:
                analysis["trend_analysis"][f"SMA_{period}"] = sma
                if current_price > sma:
                    analysis["signals"].append(f"Price above SMA_{period} - Bullish")
                else:
                    analysis["signals"].append(f"Price below SMA_{period} - Bearish")
        
        # EMA analysis
        for period in self.ema_periods:
            ema = self.calculate_ema(prices, period)
            if ema:
                analysis["trend_analysis"][f"EMA_{period}"] = ema
        
        # EMA crossover signals
        if "EMA_12" in analysis["trend_analysis"] and "EMA_26" in analysis["trend_analysis"]:
            if analysis["trend_analysis"]["EMA_12"] > analysis["trend_analysis"]["EMA_26"]:
                analysis["signals"].append("Golden Cross - Bullish EMA crossover")
            else:
                analysis["signals"].append("Death Cross - Bearish EMA crossover")
        
        # RSI analysis
        rsi = self.calculate_rsi(prices, self.rsi_period)
        if rsi:
            analysis["momentum_indicators"]["RSI"] = rsi
            if rsi > 70:
                analysis["signals"].append("RSI Overbought (>70) - Potential selling pressure")
            elif rsi < 30:
                analysis["signals"].append("RSI Oversold (<30) - Potential buying opportunity")
            elif rsi > 50:
                analysis["signals"].append("RSI above 50 - Bullish momentum")
            else:
                analysis["signals"].append("RSI below 50 - Bearish momentum")
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(prices, self.bb_period, self.bb_std)
        if bb_upper and bb_middle and bb_lower:
            analysis["volatility_indicators"]["BB_Upper"] = bb_upper
            analysis["volatility_indicators"]["BB_Middle"] = bb_middle
            analysis["volatility_indicators"]["BB_Lower"] = bb_lower
            
            if current_price > bb_upper:
                analysis["signals"].append("Price above Bollinger Upper Band - Potential overbought")
            elif current_price < bb_lower:
                analysis["signals"].append("Price below Bollinger Lower Band - Potential oversold")
            
            # Bollinger Band squeeze detection
            bb_width = (bb_upper - bb_lower) / bb_middle
            analysis["volatility_indicators"]["BB_Width"] = bb_width
            if bb_width < 0.1:  # Arbitrary threshold for squeeze
                analysis["signals"].append("Bollinger Band Squeeze - Low volatility, potential breakout")
        
        # MACD analysis
        macd_line, macd_signal, macd_histogram = self.calculate_macd(prices)
        if macd_line:
            analysis["momentum_indicators"]["MACD_Line"] = macd_line
            if macd_signal:
                analysis["momentum_indicators"]["MACD_Signal"] = macd_signal
                analysis["momentum_indicators"]["MACD_Histogram"] = macd_histogram
                
                if macd_line > macd_signal:
                    analysis["signals"].append("MACD bullish crossover")
                else:
                    analysis["signals"].append("MACD bearish crossover")
        
        # Volume analysis
        if len(self.volume_history) >= 20:
            avg_volume = sum(self.volume_history[-20:]) / 20
            if volume > avg_volume * 1.5:
                analysis["signals"].append("High volume spike - Increased interest")
            elif volume < avg_volume * 0.5:
                analysis["signals"].append("Low volume - Reduced interest")
        
        # Support and resistance levels
        if len(prices) >= 50:
            recent_prices = prices[-50:]
            analysis["support_resistance"]["resistance"] = max(recent_prices)
            analysis["support_resistance"]["support"] = min(recent_prices)
        
        return analysis
    
    def connect_websocket(self):
        """Connect to Hyperliquid WebSocket for real-time data"""
        def on_message(ws, message):
            try:
                data = json.loads(message)
                if data.get("channel") == "candle":
                    candle_data = data.get("data", [])
                    if candle_data:
                        latest_candle = candle_data[-1]
                        self.candle_data.append(latest_candle)
                        logger.info(f"Received candle data: {latest_candle}")
                        
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}")
        
        def on_error(ws, error):
            logger.error(f"WebSocket error: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            logger.info("WebSocket connection closed")
        
        def on_open(ws):
            logger.info("WebSocket connection established")
            # Subscribe to candle data
            subscription = {
                "method": "subscribe",
                "subscription": {
                    "type": "candle",
                    "coin": self.token_symbol,
                    "interval": "1m"
                }
            }
            ws.send(json.dumps(subscription))
        
        try:
            self.ws = websocket.WebSocketApp(
                self.ws_url,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open
            )
            self.ws.run_forever()
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
    
    def fetch_current_data(self) -> Tuple[float, float]:
        """Fetch current price and volume data"""
        try:
            # Get current asset context
            asset_data = self.get_spot_asset_contexts()
            if not asset_data or len(asset_data) < 2:
                logger.warning("No asset data available")
                return None, None
            
            tokens_info = asset_data[0].get("tokens", [])
            asset_contexts = asset_data[1]
            
            # Find the token index
            token_index = None
            for token in tokens_info:
                if token.get("name") == self.token_symbol:
                    token_index = token.get("index")
                    break
            
            if token_index is None:
                logger.warning(f"Token {self.token_symbol} not found")
                return None, None
            
            # Get the asset context for our token
            if token_index < len(asset_contexts):
                context = asset_contexts[token_index]
                current_price = float(context.get("markPx", 0))
                volume = float(context.get("dayNtlVlm", 0))
                return current_price, volume
            
            return None, None
            
        except Exception as e:
            logger.error(f"Error fetching current data: {e}")
            return None, None
    
    def print_analysis_report(self, analysis: Dict):
        """Print a formatted analysis report"""
        print("\n" + "="*80)
        print(f"HYPERLIQUID {analysis['token']} TECHNICAL ANALYSIS REPORT")
        print(f"Time: {analysis['timestamp']}")
        print("="*80)
        
        print(f"\n📊 CURRENT MARKET DATA:")
        print(f"Price: ${analysis['current_price']:.6f}")
        print(f"Volume (24h): ${analysis['volume']:,.2f}")
        
        if analysis['price_change_24h']:
            emoji = "🟢" if analysis['price_change_24h'] > 0 else "🔴"
            print(f"24h Change: {emoji} {analysis['price_change_24h']:.2f}%")
        
        if analysis['volume_change_24h']:
            emoji = "📈" if analysis['volume_change_24h'] > 0 else "📉"
            print(f"Volume Change: {emoji} {analysis['volume_change_24h']:.2f}%")
        
        print(f"\n📈 TREND INDICATORS:")
        for indicator, value in analysis['trend_analysis'].items():
            print(f"{indicator}: ${value:.6f}")
        
        print(f"\n⚡ MOMENTUM INDICATORS:")
        for indicator, value in analysis['momentum_indicators'].items():
            print(f"{indicator}: {value:.4f}")
        
        print(f"\n🎯 VOLATILITY INDICATORS:")
        for indicator, value in analysis['volatility_indicators'].items():
            print(f"{indicator}: {value:.6f}")
        
        if analysis['support_resistance']:
            print(f"\n🔄 SUPPORT & RESISTANCE:")
            print(f"Support: ${analysis['support_resistance'].get('support', 'N/A'):.6f}")
            print(f"Resistance: ${analysis['support_resistance'].get('resistance', 'N/A'):.6f}")
        
        print(f"\n🚨 TRADING SIGNALS:")
        for signal in analysis['signals']:
            print(f"• {signal}")
        
        print("\n" + "="*80)
    
    def run_monitoring_cycle(self):
        """Run one monitoring cycle"""
        logger.info(f"Fetching data for {self.token_symbol}...")
        
        current_price, volume = self.fetch_current_data()
        
        if current_price is None or volume is None:
            logger.warning("Unable to fetch current market data")
            return
        
        # Store historical data
        self.price_history.append(current_price)
        self.volume_history.append(volume)
        
        # Keep only last 500 data points to manage memory
        if len(self.price_history) > 500:
            self.price_history = self.price_history[-500:]
        if len(self.volume_history) > 500:
            self.volume_history = self.volume_history[-500:]
        
        # Perform technical analysis
        analysis = self.analyze_market_data(current_price, volume)
        
        # Print analysis report
        self.print_analysis_report(analysis)
        
        # Save analysis to file
        self.save_analysis_to_file(analysis)
        
        logger.info(f"Analysis complete for {self.token_symbol}")
    
    def save_analysis_to_file(self, analysis: Dict):
        """Save analysis data to a JSON file"""
        try:
            filename = f"hyperliquid_{self.token_symbol}_analysis.json"
            
            # Load existing data
            data = []
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    data = json.load(f)
            
            # Add new analysis
            data.append(analysis)
            
            # Keep only last 100 analyses
            if len(data) > 100:
                data = data[-100:]
            
            # Save back to file
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Analysis saved to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving analysis to file: {e}")
    
    def start_monitoring(self):
        """Start the monitoring process"""
        logger.info(f"Starting Hyperliquid monitor for {self.token_symbol}")
        logger.info("Monitoring every 10 minutes. Press Ctrl+C to stop.")
        
        self.running = True
        
        # Start WebSocket in a separate thread
        ws_thread = threading.Thread(target=self.connect_websocket)
        ws_thread.daemon = True
        ws_thread.start()
        
        # Initial fetch to populate some data
        logger.info("Performing initial data fetch...")
        candle_data = self.get_candle_data("1m", 100)
        if candle_data:
            for candle in candle_data:
                if isinstance(candle, dict):
                    self.price_history.append(float(candle.get('c', 0)))  # closing price
                    self.volume_history.append(float(candle.get('v', 0)))  # volume
        
        try:
            while self.running:
                self.run_monitoring_cycle()
                
                # Wait for 10 minutes (600 seconds)
                for _ in range(600):
                    if not self.running:
                        break
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
        finally:
            self.running = False
            if self.ws:
                self.ws.close()

def main():
    """Main function to run the monitor"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Hyperliquid Pump Chart Monitor")
    parser.add_argument(
        "--token", 
        default="PURR", 
        help="Token symbol to monitor (default: PURR)"
    )
    parser.add_argument(
        "--list-tokens",
        action="store_true",
        help="List available tokens and exit"
    )
    
    args = parser.parse_args()
    
    monitor = HyperliquidMonitor(args.token)
    
    if args.list_tokens:
        logger.info("Fetching available tokens...")
        metadata = monitor.get_spot_metadata()
        if metadata and "tokens" in metadata:
            print("\nAvailable tokens on Hyperliquid:")
            print("-" * 40)
            for token in metadata["tokens"]:
                print(f"• {token.get('name', 'Unknown')} (Index: {token.get('index', 'N/A')})")
        else:
            print("Unable to fetch token list")
        return
    
    try:
        monitor.start_monitoring()
    except Exception as e:
        logger.error(f"Failed to start monitoring: {e}")

if __name__ == "__main__":
    main()