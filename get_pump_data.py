#!/usr/bin/env python3
"""
Quick PUMP Token Data Fetcher from Hyperliquid
"""

import urllib.request
import json
from datetime import datetime

def get_pump_data():
    """Get current PUMP token data from Hyperliquid"""
    
    print("🔄 Fetching PUMP token data from Hyperliquid...")
    print("=" * 60)
    
    try:
        # Get asset contexts
        data = json.dumps({"type": "spotMetaAndAssetCtxs"}).encode('utf-8')
        req = urllib.request.Request(
            "https://api.hyperliquid.xyz/info",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            asset_data = json.loads(response.read())
        
        if len(asset_data) < 2:
            print("❌ No asset data available")
            return
        
        tokens_info = asset_data[0].get("tokens", [])
        asset_contexts = asset_data[1]
        
        # Find PUMP token
        pump_index = None
        for token in tokens_info:
            if token.get("name") == "PUMP":
                pump_index = token.get("index")
                break
        
        if pump_index is None:
            print("❌ PUMP token not found")
            return
        
        # Get PUMP data
        if pump_index < len(asset_contexts):
            pump_data = asset_contexts[pump_index]
            
            current_price = float(pump_data.get("markPx", 0))
            volume_24h = float(pump_data.get("dayNtlVlm", 0))
            prev_price = float(pump_data.get("prevDayPx", 0))
            mid_price = pump_data.get("midPx", "N/A")
            
            # Calculate 24h change
            if prev_price > 0:
                price_change = ((current_price - prev_price) / prev_price) * 100
            else:
                price_change = 0
            
            # Display results
            print("💰 PUMP TOKEN DATA FROM HYPERLIQUID")
            print("=" * 60)
            print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"💵 Current Price: ${current_price:.8f}")
            print(f"📊 Mid Price: ${mid_price}")
            print(f"📈 Previous Day Price: ${prev_price:.8f}")
            
            # Price change with emoji
            if price_change > 0:
                print(f"📈 24h Change: 🟢 +{price_change:.2f}%")
            elif price_change < 0:
                print(f"📉 24h Change: 🔴 {price_change:.2f}%")
            else:
                print(f"⚖️  24h Change: {price_change:.2f}%")
            
            print(f"💧 24h Volume: ${volume_24h:,.2f}")
            print(f"🆔 Token Index: {pump_index}")
            
            # Basic analysis
            print("\n🔍 QUICK ANALYSIS:")
            if price_change > 5:
                print("   🚀 Strong bullish movement (+5%+)")
            elif price_change > 2:
                print("   📈 Moderate bullish movement (+2% to +5%)")
            elif price_change > 0:
                print("   🟢 Slight bullish movement (0% to +2%)")
            elif price_change > -2:
                print("   ⚖️  Sideways movement (-2% to 0%)")
            elif price_change > -5:
                print("   📉 Moderate bearish movement (-5% to -2%)")
            else:
                print("   🔻 Strong bearish movement (-5% or more)")
            
            if volume_24h > 1000:
                print("   💪 Good trading volume")
            elif volume_24h > 100:
                print("   📊 Moderate trading volume")
            else:
                print("   🤏 Low trading volume")
            
            print("=" * 60)
            
            return {
                "price": current_price,
                "volume": volume_24h,
                "change": price_change,
                "prev_price": prev_price
            }
        
    except Exception as e:
        print(f"❌ Error fetching PUMP data: {e}")
        return None

def get_top_volume_tokens():
    """Get top tokens by volume for context"""
    
    print("\n📊 TOP VOLUME TOKENS (for context):")
    print("-" * 40)
    
    try:
        data = json.dumps({"type": "spotMetaAndAssetCtxs"}).encode('utf-8')
        req = urllib.request.Request(
            "https://api.hyperliquid.xyz/info",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            asset_data = json.loads(response.read())
        
        tokens_info = asset_data[0].get("tokens", [])
        asset_contexts = asset_data[1]
        
        # Create list of tokens with volume
        token_volumes = []
        for i, context in enumerate(asset_contexts):
            if i < len(tokens_info):
                token_name = tokens_info[i].get("name", f"Token_{i}")
                volume = float(context.get("dayNtlVlm", 0))
                price = float(context.get("markPx", 0))
                if volume > 0:  # Only include tokens with volume
                    token_volumes.append((token_name, volume, price))
        
        # Sort by volume and show top 10
        token_volumes.sort(key=lambda x: x[1], reverse=True)
        
        for i, (name, volume, price) in enumerate(token_volumes[:10]):
            print(f"{i+1:2}. {name:12} | Volume: ${volume:>12,.2f} | Price: ${price:.6f}")
        
    except Exception as e:
        print(f"❌ Error fetching top tokens: {e}")

if __name__ == "__main__":
    pump_data = get_pump_data()
    get_top_volume_tokens()
    
    print(f"\n✅ Data fetch complete at {datetime.now().strftime('%H:%M:%S')}")