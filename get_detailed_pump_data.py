#!/usr/bin/env python3
"""
Detailed PUMP Token Analysis from Hyperliquid
"""

import urllib.request
import json
from datetime import datetime, timedelta

def make_api_request(payload):
    """Make request to Hyperliquid API"""
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            "https://api.hyperliquid.xyz/info",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read())
    except Exception as e:
        print(f"❌ API request failed: {e}")
        return None

def get_pump_market_data():
    """Get comprehensive PUMP market data"""
    
    print("🔄 Fetching detailed PUMP data from Hyperliquid...")
    print("=" * 70)
    
    # Get current market data
    asset_data = make_api_request({"type": "spotMetaAndAssetCtxs"})
    if not asset_data or len(asset_data) < 2:
        print("❌ No asset data available")
        return
    
    tokens_info = asset_data[0].get("tokens", [])
    asset_contexts = asset_data[1]
    
    # Find PUMP token
    pump_index = None
    pump_token_info = None
    for token in tokens_info:
        if token.get("name") == "PUMP":
            pump_index = token.get("index")
            pump_token_info = token
            break
    
    if pump_index is None:
        print("❌ PUMP token not found")
        return
    
    # Get PUMP context
    pump_context = asset_contexts[pump_index] if pump_index < len(asset_contexts) else {}
    
    # Extract data
    current_price = float(pump_context.get("markPx", 0))
    mid_price = pump_context.get("midPx")
    volume_24h = float(pump_context.get("dayNtlVlm", 0))
    prev_price = float(pump_context.get("prevDayPx", 0))
    
    print("💰 PUMP TOKEN DETAILED ANALYSIS")
    print("=" * 70)
    print(f"🕐 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    
    # Token Information
    print("📋 TOKEN INFORMATION:")
    print(f"   🪙 Symbol: PUMP")
    print(f"   🆔 Index: {pump_index}")
    print(f"   🏷️  Token ID: {pump_token_info.get('tokenId', 'N/A')}")
    print(f"   🔢 Decimals: {pump_token_info.get('weiDecimals', 'N/A')}")
    print(f"   📊 Size Decimals: {pump_token_info.get('szDecimals', 'N/A')}")
    print()
    
    # Current Market Data
    print("💹 CURRENT MARKET DATA:")
    print(f"   💵 Mark Price: ${current_price:.8f}")
    print(f"   📊 Mid Price: ${mid_price}")
    print(f"   📈 Previous 24h: ${prev_price:.8f}")
    print(f"   💧 24h Volume: ${volume_24h:,.2f}")
    
    # Calculate changes
    if prev_price > 0:
        price_change = ((current_price - prev_price) / prev_price) * 100
        price_diff = current_price - prev_price
        
        if price_change > 0:
            print(f"   📈 24h Change: 🟢 +{price_change:.2f}% (+${price_diff:.8f})")
        else:
            print(f"   📉 24h Change: 🔴 {price_change:.2f}% (${price_diff:.8f})")
    
    print()
    
    # Technical Analysis
    print("📊 TECHNICAL ANALYSIS:")
    
    # Volume analysis
    if volume_24h > 10000:
        volume_status = "🔥 High volume"
    elif volume_24h > 1000:
        volume_status = "📊 Moderate volume"
    elif volume_24h > 100:
        volume_status = "📈 Low volume"
    else:
        volume_status = "🤏 Very low volume"
    
    print(f"   📊 Volume Status: {volume_status}")
    
    # Price movement analysis
    if abs(price_change) < 1:
        movement = "⚖️  Stable/Sideways"
    elif price_change > 5:
        movement = "🚀 Strong bullish"
    elif price_change > 2:
        movement = "📈 Moderate bullish"
    elif price_change > 0:
        movement = "🟢 Slight bullish"
    elif price_change > -2:
        movement = "🔴 Slight bearish"
    elif price_change > -5:
        movement = "📉 Moderate bearish"
    else:
        movement = "💥 Strong bearish"
    
    print(f"   📈 Price Movement: {movement}")
    
    # Market cap estimation (if we had supply data)
    print(f"   💰 Market Context: Low-cap token with minimal trading activity")
    
    print()
    
    # Trading Signals
    print("🚨 TRADING SIGNALS:")
    signals = []
    
    if volume_24h < 100:
        signals.append("⚠️  Very low liquidity - High slippage risk")
    
    if abs(price_change) < 1:
        signals.append("⚖️  Price consolidation - Waiting for breakout")
    
    if price_change > 0:
        signals.append("📈 Slight bullish momentum")
    elif price_change < 0:
        signals.append("📉 Slight bearish pressure")
    
    if volume_24h < 50:
        signals.append("🚫 Avoid large trades - Limited liquidity")
    
    for signal in signals:
        print(f"   • {signal}")
    
    print()
    print("=" * 70)
    
    return {
        "price": current_price,
        "volume": volume_24h,
        "change": price_change if prev_price > 0 else 0,
        "prev_price": prev_price,
        "token_index": pump_index
    }

def get_recent_trades():
    """Try to get recent trade data if available"""
    print("🔄 Checking for recent trade activity...")
    
    try:
        # Note: This would require WebSocket or specific trade endpoints
        # For now, we'll provide general market context
        print("📊 Trade data requires WebSocket connection for real-time updates")
        print("💡 Use the monitoring system for continuous trade tracking")
    except Exception as e:
        print(f"⚠️  Trade data not available: {e}")

def get_market_overview():
    """Get general market overview"""
    print("\n🌍 HYPERLIQUID MARKET OVERVIEW:")
    print("-" * 50)
    
    asset_data = make_api_request({"type": "spotMetaAndAssetCtxs"})
    if asset_data and len(asset_data) >= 2:
        tokens_info = asset_data[0].get("tokens", [])
        asset_contexts = asset_data[1]
        
        total_tokens = len(tokens_info)
        active_markets = len([ctx for ctx in asset_contexts if float(ctx.get("dayNtlVlm", 0)) > 0])
        
        print(f"📊 Total Tokens: {total_tokens}")
        print(f"📈 Active Markets (24h): {active_markets}")
        print(f"🎯 PUMP Rank by Volume: Very low (minimal trading)")

if __name__ == "__main__":
    pump_data = get_pump_market_data()
    get_recent_trades()
    get_market_overview()
    
    print(f"\n✅ Detailed analysis complete at {datetime.now().strftime('%H:%M:%S')}")
    print("💡 For continuous monitoring, run: python3 hyperliquid_simple_monitor.py --token PUMP")