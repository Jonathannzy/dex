#!/usr/bin/env python3
"""
Hyperliquid Simple Monitor - Works with built-in libraries only
Monitors pump chart data every 10 minutes with basic technical analysis
"""

import urllib.request
import json
import time
import signal
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

class SimpleHyperliquidMonitor:
    def __init__(self, token_symbol: str = "PURR"):
        self.token_symbol = token_symbol
        self.base_url = "https://api.hyperliquid.xyz"
        self.price_history = []
        self.volume_history = []
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print(f"🚀 Initializing monitor for {token_symbol} token")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n⚠️  Received shutdown signal. Stopping monitor...")
        self.running = False
        sys.exit(0)
    
    def make_api_request(self, payload: Dict) -> Optional[Dict]:
        """Make a request to Hyperliquid API"""
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                f"{self.base_url}/info",
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read())
                
        except Exception as e:
            print(f"❌ API request failed: {e}")
            return None
    
    def get_current_data(self) -> Tuple[Optional[float], Optional[float]]:
        """Get current price and volume for the token"""
        
        # Get asset contexts
        asset_data = self.make_api_request({"type": "spotMetaAndAssetCtxs"})
        if not asset_data or len(asset_data) < 2:
            print("⚠️  No asset data available")
            return None, None
        
        tokens_info = asset_data[0].get("tokens", [])
        asset_contexts = asset_data[1]
        
        # Find token index
        token_index = None
        for token in tokens_info:
            if token.get("name") == self.token_symbol:
                token_index = token.get("index")
                break
        
        if token_index is None:
            print(f"⚠️  Token {self.token_symbol} not found")
            return None, None
        
        # Get market data
        if token_index < len(asset_contexts):
            context = asset_contexts[token_index]
            price = float(context.get("markPx", 0))
            volume = float(context.get("dayNtlVlm", 0))
            prev_price = float(context.get("prevDayPx", 0))
            
            return price, volume, prev_price
        
        return None, None, None
    
    def calculate_sma(self, prices: List[float], period: int) -> Optional[float]:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return None
        return sum(prices[-period:]) / period
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> Optional[float]:
        """Calculate basic RSI"""
        if len(prices) < period + 1:
            return None
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(-change)
        
        if len(gains) < period:
            return None
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def analyze_trend(self, prices: List[float]) -> str:
        """Simple trend analysis"""
        if len(prices) < 3:
            return "Insufficient data"
        
        recent = prices[-3:]
        if recent[2] > recent[1] > recent[0]:
            return "Strong Uptrend"
        elif recent[2] > recent[0]:
            return "Uptrend"
        elif recent[2] < recent[1] < recent[0]:
            return "Strong Downtrend"
        elif recent[2] < recent[0]:
            return "Downtrend"
        else:
            return "Sideways"
    
    def generate_signals(self, price: float, volume: float, prev_price: Optional[float] = None) -> List[str]:
        """Generate trading signals based on analysis"""
        signals = []
        
        # Price change analysis
        if prev_price and prev_price > 0:
            price_change = ((price - prev_price) / prev_price) * 100
            if price_change > 5:
                signals.append(f"🚀 Strong daily gain: +{price_change:.2f}%")
            elif price_change > 2:
                signals.append(f"📈 Good daily gain: +{price_change:.2f}%")
            elif price_change < -5:
                signals.append(f"🔻 Strong daily loss: {price_change:.2f}%")
            elif price_change < -2:
                signals.append(f"📉 Daily loss: {price_change:.2f}%")
            else:
                signals.append(f"⚖️  Daily change: {price_change:.2f}%")
        
        # Volume analysis
        if len(self.volume_history) >= 5:
            avg_volume = sum(self.volume_history[-5:]) / 5
            if volume > avg_volume * 1.5:
                signals.append("📊 High volume spike - Increased interest")
            elif volume < avg_volume * 0.5:
                signals.append("📊 Low volume - Reduced activity")
        
        # Moving average signals
        if len(self.price_history) >= 20:
            sma_9 = self.calculate_sma(self.price_history, 9)
            sma_20 = self.calculate_sma(self.price_history, 20)
            
            if sma_9 and sma_20:
                if price > sma_9 > sma_20:
                    signals.append("🔥 Price above both MA9 and MA20 - Strong bullish")
                elif price > sma_9:
                    signals.append("📈 Price above MA9 - Short-term bullish")
                elif price < sma_9 and sma_9 < sma_20:
                    signals.append("❄️  Price below both MA9 and MA20 - Strong bearish")
                elif price < sma_9:
                    signals.append("📉 Price below MA9 - Short-term bearish")
        
        # RSI signals
        if len(self.price_history) >= 15:
            rsi = self.calculate_rsi(self.price_history)
            if rsi:
                if rsi > 70:
                    signals.append(f"⚠️  RSI overbought: {rsi:.1f} - Potential sell signal")
                elif rsi < 30:
                    signals.append(f"💎 RSI oversold: {rsi:.1f} - Potential buy signal")
                elif rsi > 50:
                    signals.append(f"💪 RSI bullish: {rsi:.1f}")
                else:
                    signals.append(f"🤔 RSI bearish: {rsi:.1f}")
        
        # Trend analysis
        trend = self.analyze_trend(self.price_history)
        signals.append(f"📊 Trend: {trend}")
        
        # Support/Resistance
        if len(self.price_history) >= 20:
            recent_prices = self.price_history[-20:]
            resistance = max(recent_prices)
            support = min(recent_prices)
            
            distance_to_resistance = ((resistance - price) / price) * 100
            distance_to_support = ((price - support) / price) * 100
            
            if distance_to_resistance < 2:
                signals.append(f"🚧 Near resistance level: ${resistance:.6f}")
            if distance_to_support < 2:
                signals.append(f"🛡️  Near support level: ${support:.6f}")
        
        return signals
    
    def print_analysis(self, price: float, volume: float, prev_price: Optional[float] = None):
        """Print comprehensive analysis"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("\n" + "="*70)
        print(f"📊 HYPERLIQUID {self.token_symbol} ANALYSIS REPORT")
        print(f"🕐 Time: {timestamp}")
        print("="*70)
        
        # Current market data
        print(f"\n💰 CURRENT PRICE: ${price:.6f}")
        print(f"📊 24H VOLUME: ${volume:,.2f}")
        
        if prev_price:
            change = ((price - prev_price) / prev_price) * 100
            emoji = "🟢" if change >= 0 else "🔴"
            print(f"📈 24H CHANGE: {emoji} {change:+.2f}%")
        
        # Technical indicators
        if len(self.price_history) >= 9:
            sma_9 = self.calculate_sma(self.price_history, 9)
            if sma_9:
                print(f"📈 SMA(9): ${sma_9:.6f}")
        
        if len(self.price_history) >= 20:
            sma_20 = self.calculate_sma(self.price_history, 20)
            if sma_20:
                print(f"📈 SMA(20): ${sma_20:.6f}")
        
        if len(self.price_history) >= 15:
            rsi = self.calculate_rsi(self.price_history)
            if rsi:
                print(f"⚡ RSI(14): {rsi:.2f}")
        
        # Support and resistance
        if len(self.price_history) >= 10:
            recent = self.price_history[-10:]
            print(f"🛡️  Recent Support: ${min(recent):.6f}")
            print(f"🚧 Recent Resistance: ${max(recent):.6f}")
        
        # Signals
        signals = self.generate_signals(price, volume, prev_price)
        print(f"\n🚨 TRADING SIGNALS:")
        for signal in signals:
            print(f"   • {signal}")
        
        print("\n" + "="*70)
    
    def save_data(self, price: float, volume: float):
        """Save data to a simple file"""
        try:
            filename = f"hyperliquid_{self.token_symbol}_data.txt"
            timestamp = datetime.now().isoformat()
            
            with open(filename, "a") as f:
                f.write(f"{timestamp},{price},{volume}\n")
                
        except Exception as e:
            print(f"⚠️  Could not save data: {e}")
    
    def run_cycle(self):
        """Run one monitoring cycle"""
        print(f"\n🔄 Fetching data for {self.token_symbol}...")
        
        result = self.get_current_data()
        if len(result) == 3:
            price, volume, prev_price = result
        else:
            price, volume = result[0], result[1]
            prev_price = None
        
        if price is None or volume is None:
            print("❌ Failed to fetch current data")
            return
        
        # Store data
        self.price_history.append(price)
        self.volume_history.append(volume)
        
        # Keep last 100 data points
        if len(self.price_history) > 100:
            self.price_history = self.price_history[-100:]
        if len(self.volume_history) > 100:
            self.volume_history = self.volume_history[-100:]
        
        # Analysis and display
        self.print_analysis(price, volume, prev_price)
        
        # Save data
        self.save_data(price, volume)
        
        print(f"✅ Analysis complete. Next update in 10 minutes.")
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        print(f"\n🚀 Starting Hyperliquid monitor for {self.token_symbol}")
        print("⏰ Updates every 10 minutes. Press Ctrl+C to stop.\n")
        
        self.running = True
        
        try:
            while self.running:
                self.run_cycle()
                
                # Wait 10 minutes (600 seconds)
                print("⏳ Waiting 10 minutes for next update...")
                for i in range(600):
                    if not self.running:
                        break
                    time.sleep(1)
                    # Show countdown every 60 seconds
                    if i % 60 == 0 and i > 0:
                        remaining_minutes = (600 - i) // 60
                        print(f"⏱️  {remaining_minutes} minutes until next update...")
                        
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Error in monitoring loop: {e}")
        finally:
            self.running = False
            print("👋 Monitor stopped")

def list_available_tokens():
    """List available tokens"""
    print("🔍 Fetching available tokens...")
    
    try:
        data = json.dumps({"type": "spotMeta"}).encode('utf-8')
        req = urllib.request.Request(
            "https://api.hyperliquid.xyz/info",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            metadata = json.loads(response.read())
            
        tokens = metadata.get('tokens', [])
        print(f"\n📊 Found {len(tokens)} tokens on Hyperliquid:")
        print("-" * 50)
        
        # Show tokens in columns
        for i, token in enumerate(tokens[:50]):  # Show first 50
            name = token.get('name', 'Unknown')
            index = token.get('index', 'N/A')
            print(f"{name:12} (Index: {index:3})", end="")
            if (i + 1) % 3 == 0:
                print()  # New line every 3 tokens
        
        if len(tokens) > 50:
            print(f"\n... and {len(tokens) - 50} more tokens")
            
        print(f"\n💡 Usage: python3 {sys.argv[0]} --token TOKEN_NAME")
        
    except Exception as e:
        print(f"❌ Error fetching tokens: {e}")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Simple Hyperliquid Pump Monitor - Basic TA every 10 minutes"
    )
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
    
    if args.list_tokens:
        list_available_tokens()
        return
    
    try:
        monitor = SimpleHyperliquidMonitor(args.token)
        monitor.start_monitoring()
    except Exception as e:
        print(f"❌ Failed to start monitoring: {e}")

if __name__ == "__main__":
    main()