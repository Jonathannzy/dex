#!/usr/bin/env python3
"""
Hyperliquid API Test - Basic functionality check
"""

import urllib.request
import urllib.parse
import json
import time
from datetime import datetime

def test_hyperliquid_api():
    """Test basic connectivity to Hyperliquid API"""
    
    base_url = "https://api.hyperliquid.xyz"
    
    print("🔄 Testing Hyperliquid API Connection...")
    print("=" * 50)
    
    # Test 1: Get spot metadata
    try:
        print("\n1. Fetching spot metadata...")
        
        data = json.dumps({"type": "spotMeta"}).encode('utf-8')
        req = urllib.request.Request(
            f"{base_url}/info",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            metadata = json.loads(response.read())
            
        print("✅ Successfully connected to Hyperliquid API!")
        print(f"📊 Found {len(metadata.get('tokens', []))} tokens available")
        
        # List first 10 tokens
        tokens = metadata.get('tokens', [])[:10]
        print("\n🪙 Available tokens (first 10):")
        for token in tokens:
            print(f"   • {token.get('name', 'Unknown')} (Index: {token.get('index', 'N/A')})")
            
    except Exception as e:
        print(f"❌ Error fetching metadata: {e}")
        return False
    
    # Test 2: Get current market data
    try:
        print("\n2. Fetching current market data...")
        
        data = json.dumps({"type": "spotMetaAndAssetCtxs"}).encode('utf-8')
        req = urllib.request.Request(
            f"{base_url}/info",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as response:
            asset_data = json.loads(response.read())
            
        if len(asset_data) >= 2:
            tokens_info = asset_data[0].get('tokens', [])
            asset_contexts = asset_data[1]
            
            print("✅ Successfully fetched market data!")
            print(f"📈 Market data for {len(asset_contexts)} assets")
            
            # Show data for first few tokens
            for i, context in enumerate(asset_contexts[:3]):
                if i < len(tokens_info):
                    token_name = tokens_info[i].get('name', f'Token_{i}')
                    price = context.get('markPx', 'N/A')
                    volume = context.get('dayNtlVlm', 'N/A')
                    print(f"   💰 {token_name}: ${price} (Volume: ${volume})")
                    
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        return False
    
    # Test 3: Check if PURR token exists and get its data
    try:
        print("\n3. Looking for PURR token...")
        
        purr_found = False
        purr_index = None
        
        for token in tokens_info:
            if token.get('name') == 'PURR':
                purr_found = True
                purr_index = token.get('index')
                break
        
        if purr_found and purr_index is not None and purr_index < len(asset_contexts):
            purr_data = asset_contexts[purr_index]
            print("✅ PURR token found!")
            print(f"   💰 Price: ${purr_data.get('markPx', 'N/A')}")
            print(f"   📊 24h Volume: ${purr_data.get('dayNtlVlm', 'N/A')}")
            print(f"   📈 Previous Day Price: ${purr_data.get('prevDayPx', 'N/A')}")
        else:
            print("⚠️  PURR token not found, will look for alternative...")
            
            # Try to find any token with good volume
            best_token = None
            best_volume = 0
            
            for i, context in enumerate(asset_contexts):
                try:
                    volume = float(context.get('dayNtlVlm', 0))
                    if volume > best_volume and i < len(tokens_info):
                        best_volume = volume
                        best_token = tokens_info[i].get('name')
                except:
                    continue
            
            if best_token:
                print(f"   📈 Suggested token to monitor: {best_token} (${best_volume:,.2f} volume)")
            
    except Exception as e:
        print(f"❌ Error checking PURR token: {e}")
    
    print("\n" + "=" * 50)
    print("✅ API Test Complete!")
    print(f"🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return True

def suggest_usage():
    """Provide usage suggestions"""
    
    print("\n🚀 Next Steps:")
    print("-" * 30)
    print("1. Install dependencies in a virtual environment:")
    print("   sudo apt install python3.13-venv  # If needed")
    print("   python3 -m venv venv")
    print("   source venv/bin/activate")
    print("   pip install -r requirements.txt")
    print()
    print("2. Run the full monitoring system:")
    print("   python3 hyperliquid_monitor.py --list-tokens")
    print("   python3 hyperliquid_monitor.py --token PURR")
    print()
    print("3. Monitor any available token:")
    print("   python3 hyperliquid_monitor.py --token HYPE")
    print("   python3 hyperliquid_monitor.py --token <TOKEN_NAME>")

if __name__ == "__main__":
    print("🔍 Hyperliquid API Connection Test")
    print("=" * 50)
    
    success = test_hyperliquid_api()
    
    if success:
        suggest_usage()
    else:
        print("\n❌ API test failed. Please check your internet connection.")