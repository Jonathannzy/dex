#!/usr/bin/env python3
"""
Simple test of the ticker extraction functionality
"""

import re
from typing import List, Dict, Set

# Simple ticker extractor without external dependencies
class SimpleTicker:
    def __init__(self):
        self.crypto_symbols = {
            'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'MATIC', 'DOT', 'AVAX',
            'SHIB', 'LTC', 'ATOM', 'UNI', 'LINK', 'XMR', 'BCH', 'ETC', 'FIL', 'ICP',
            'APT', 'NEAR', 'VET', 'ALGO', 'FLOW', 'MANA', 'SAND', 'AXS', 'CHZ', 'ENJ',
            'ALPHA', 'COMP', 'AAVE', 'CRV', 'SUSHI', 'YFI', 'SNX', 'MKR'
        }
        self.cashtag_pattern = re.compile(r'\$([A-Z]{2,10})')
    
    def extract_tickers(self, text: str) -> List[str]:
        """Extract cryptocurrency tickers from text"""
        tickers = []
        
        # Extract cashtags ($BTC, $ETH, etc.)
        cashtags = self.cashtag_pattern.findall(text.upper())
        for tag in cashtags:
            if tag in self.crypto_symbols:
                tickers.append(tag)
        
        return list(set(tickers))  # Remove duplicates

def analyze_sentiment(text: str) -> str:
    """Simple sentiment analysis"""
    bullish_words = ['moon', 'pump', 'bull', 'buy', 'bullish', 'gem', 'alpha', 'rocket', 'diamond hands', 'hodl']
    bearish_words = ['dump', 'bear', 'sell', 'bearish', 'crash', 'paper hands', 'rug', 'scam']
    
    text_lower = text.lower()
    bullish_count = sum(1 for word in bullish_words if word in text_lower)
    bearish_count = sum(1 for word in bearish_words if word in text_lower)
    
    if bullish_count > bearish_count:
        return 'bullish'
    elif bearish_count > bullish_count:
        return 'bearish'
    else:
        return 'neutral'

def test_functionality():
    """Test the core functionality"""
    print("🚀 Crypto X Analyzer - Simple Test")
    print("=" * 50)
    
    # Test tweets
    test_tweets = [
        '$BTC looking strong above 42k! This bull run is just getting started 🚀',
        'Hidden gem alert 🚨 $ALPHA is still under the radar. Low cap, solid fundamentals',
        '$ETH gas fees are killing me. Time to look into $MATIC',
        'DeFi summer is back! $UNI, $AAVE, $COMP all pumping',
        'Warning: $SCAMCOIN looks like a rug pull. Avoid at all costs!',
        '$SOL ecosystem is on fire 🔥',
        'Altseason incoming? $BTC dominance dropping',
        '$DOGE to the moon! 🌙 Diamond hands!'
    ]
    
    ticker_extractor = SimpleTicker()
    
    print("📊 Analyzing test tweets...")
    print()
    
    all_tickers = []
    sentiments = []
    
    for i, tweet in enumerate(test_tweets, 1):
        print(f"Tweet {i}: {tweet}")
        
        # Extract tickers
        tickers = ticker_extractor.extract_tickers(tweet)
        print(f"  Tickers: {tickers}")
        
        # Analyze sentiment
        sentiment = analyze_sentiment(tweet)
        print(f"  Sentiment: {sentiment}")
        print()
        
        all_tickers.extend(tickers)
        sentiments.append(sentiment)
    
    # Summary
    print("=" * 50)
    print("📈 SUMMARY")
    print("=" * 50)
    
    # Count tickers
    from collections import Counter
    ticker_counts = Counter(all_tickers)
    
    print("🪙 Most mentioned tickers:")
    for ticker, count in ticker_counts.most_common(5):
        print(f"  ${ticker}: {count} mentions")
    
    print()
    
    # Count sentiments
    sentiment_counts = Counter(sentiments)
    print("😊 Sentiment distribution:")
    for sentiment, count in sentiment_counts.items():
        print(f"  {sentiment.title()}: {count}")
    
    print()
    print("✅ Test completed successfully!")
    print("🔗 This demonstrates the core functionality of the Crypto X Analyzer")
    print("📱 To use with real Twitter data, configure API keys and run the full app")

if __name__ == "__main__":
    test_functionality()