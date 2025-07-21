#!/usr/bin/env python3
"""
Single PUMP Analysis Cycle - Shows what the continuous monitor does
"""

import urllib.request
import json
from datetime import datetime

class PumpAnalyzer:
    def __init__(self):
        self.base_url = "https://api.hyperliquid.xyz"
        self.token_symbol = "PUMP"
        
    def make_api_request(self, payload):
        """Make request to Hyperliquid API"""
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
    
    def get_current_data(self):
        """Get current PUMP data"""
        asset_data = self.make_api_request({"type": "spotMetaAndAssetCtxs"})
        if not asset_data or len(asset_data) < 2:
            return None, None, None
        
        tokens_info = asset_data[0].get("tokens", [])
        asset_contexts = asset_data[1]
        
        # Find PUMP token
        pump_index = None
        for token in tokens_info:
            if token.get("name") == self.token_symbol:
                pump_index = token.get("index")
                break
        
        if pump_index is None or pump_index >= len(asset_contexts):
            return None, None, None
        
        context = asset_contexts[pump_index]
        price = float(context.get("markPx", 0))
        volume = float(context.get("dayNtlVlm", 0))
        prev_price = float(context.get("prevDayPx", 0))
        
        return price, volume, prev_price
    
    def generate_signals(self, price, volume, prev_price):
        """Generate trading signals"""
        signals = []
        
        if prev_price > 0:
            price_change = ((price - prev_price) / prev_price) * 100
            
            if price_change > 5:
                signals.append("🚀 Strong daily gain: +{:.2f}%".format(price_change))
            elif price_change > 2:
                signals.append("📈 Good daily gain: +{:.2f}%".format(price_change))
            elif price_change > 0:
                signals.append("🟢 Slight daily gain: +{:.2f}%".format(price_change))
            elif price_change > -2:
                signals.append("⚖️ Minor daily change: {:.2f}%".format(price_change))
            elif price_change > -5:
                signals.append("📉 Moderate daily loss: {:.2f}%".format(price_change))
            else:
                signals.append("🔻 Strong daily loss: {:.2f}%".format(price_change))
        
        # Volume analysis
        if volume > 10000:
            signals.append("📊 High volume spike - Major interest")
        elif volume > 1000:
            signals.append("📊 Good volume - Moderate interest")
        elif volume > 100:
            signals.append("📊 Low volume - Limited interest")
        else:
            signals.append("📊 Very low volume - Minimal trading")
        
        # Liquidity warnings
        if volume < 100:
            signals.append("⚠️ Low liquidity - High slippage risk")
        
        if volume < 50:
            signals.append("🚫 Avoid large trades - Very limited liquidity")
        
        return signals
    
    def print_analysis(self, price, volume, prev_price):
        """Print complete analysis report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        print("\n" + "="*70)
        print(f"📊 HYPERLIQUID PUMP LIVE ANALYSIS")
        print(f"🕐 Time: {timestamp}")
        print("="*70)
        
        # Current data
        print(f"\n💰 CURRENT PRICE: ${price:.8f}")
        print(f"📊 24H VOLUME: ${volume:,.2f}")
        
        if prev_price > 0:
            change = ((price - prev_price) / prev_price) * 100
            change_value = price - prev_price
            emoji = "🟢" if change >= 0 else "🔴"
            print(f"📈 24H CHANGE: {emoji} {change:+.2f}% (${change_value:+.8f})")
            print(f"📉 PREVIOUS PRICE: ${prev_price:.8f}")
        
        # Market assessment
        print(f"\n🎯 MARKET ASSESSMENT:")
        
        if volume < 50:
            liquidity_status = "🔴 Critical - Very low liquidity"
        elif volume < 200:
            liquidity_status = "🟡 Warning - Low liquidity"
        elif volume < 1000:
            liquidity_status = "🟢 Moderate liquidity"
        else:
            liquidity_status = "🟢 Good liquidity"
        
        print(f"   💧 Liquidity: {liquidity_status}")
        
        if abs(change) < 1:
            volatility = "🟢 Low volatility - Stable"
        elif abs(change) < 5:
            volatility = "🟡 Moderate volatility"
        else:
            volatility = "🔴 High volatility"
            
        print(f"   📊 Volatility: {volatility}")
        
        # Trading signals
        signals = self.generate_signals(price, volume, prev_price)
        print(f"\n🚨 TRADING SIGNALS:")
        for signal in signals:
            print(f"   • {signal}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if volume < 100:
            print("   • ⚠️ Wait for higher volume before trading")
            print("   • 🔍 Monitor for volume spikes indicating interest")
            print("   • 📊 Consider this a low-activity period")
        else:
            print("   • ✅ Sufficient liquidity for small trades")
            print("   • 📈 Monitor price action for trends")
        
        if abs(change) < 2:
            print("   • ⚖️ Price in consolidation phase")
            print("   • 🎯 Watch for breakout signals")
        
        print("\n" + "="*70)
    
    def run_analysis(self):
        """Run complete analysis"""
        print("🚀 PUMP TOKEN LIVE ANALYSIS")
        print("🔄 Fetching data from Hyperliquid...")
        
        price, volume, prev_price = self.get_current_data()
        
        if price is None:
            print("❌ Failed to fetch PUMP data")
            return
        
        self.print_analysis(price, volume, prev_price)
        
        print("\n💡 This is what the continuous monitor shows every 10 minutes!")
        print("⚡ To run continuously: python3 hyperliquid_simple_monitor.py --token PUMP")

if __name__ == "__main__":
    analyzer = PumpAnalyzer()
    analyzer.run_analysis()