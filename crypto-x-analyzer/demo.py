"""
Demo script for Crypto X Analyzer
This shows the functionality without requiring real API keys
"""

import json
from datetime import datetime, timedelta
import random

from services.analytics_service import AnalyticsService
from utils.ticker_extractor import TickerExtractor

def generate_demo_tweets():
    """Generate realistic demo tweets for demonstration"""
    demo_tweets = [
        {
            'id': '1',
            'text': '$BTC looking strong above 42k! This bull run is just getting started 🚀 #Bitcoin',
            'created_at': datetime.now() - timedelta(hours=2),
            'author_id': 'user1',
            'like_count': 45,
            'retweet_count': 12,
            'reply_count': 8,
            'quote_count': 3
        },
        {
            'id': '2',
            'text': 'Hidden gem alert 🚨 $ALPHA is still under the radar. Low cap, solid fundamentals. DYOR but this could be huge',
            'created_at': datetime.now() - timedelta(hours=4),
            'author_id': 'user2',
            'like_count': 156,
            'retweet_count': 45,
            'reply_count': 23,
            'quote_count': 7
        },
        {
            'id': '3',
            'text': '$ETH gas fees are killing me. Time to look into some Layer 2 solutions like $MATIC',
            'created_at': datetime.now() - timedelta(hours=6),
            'author_id': 'user3',
            'like_count': 89,
            'retweet_count': 31,
            'reply_count': 15,
            'quote_count': 5
        },
        {
            'id': '4',
            'text': 'DeFi summer is back! $UNI, $AAVE, $COMP all pumping. The yield farming opportunities are insane right now',
            'created_at': datetime.now() - timedelta(hours=8),
            'author_id': 'user4',
            'like_count': 203,
            'retweet_count': 78,
            'reply_count': 45,
            'quote_count': 12
        },
        {
            'id': '5',
            'text': 'Warning: $SCAMCOIN looks like a rug pull. Team is anonymous, no real utility. Avoid at all costs!',
            'created_at': datetime.now() - timedelta(hours=10),
            'author_id': 'user5',
            'like_count': 67,
            'retweet_count': 34,
            'reply_count': 19,
            'quote_count': 8
        },
        {
            'id': '6',
            'text': '$SOL ecosystem is on fire 🔥 The speed and low fees make it a serious competitor to Ethereum',
            'created_at': datetime.now() - timedelta(hours=12),
            'author_id': 'user6',
            'like_count': 134,
            'retweet_count': 56,
            'reply_count': 28,
            'quote_count': 9
        },
        {
            'id': '7',
            'text': 'Altseason incoming? $BTC dominance dropping and alts starting to pump. Time to rotate some profits',
            'created_at': datetime.now() - timedelta(hours=14),
            'author_id': 'user7',
            'like_count': 91,
            'retweet_count': 43,
            'reply_count': 21,
            'quote_count': 6
        },
        {
            'id': '8',
            'text': 'NFT project @coolapes launching tomorrow. Heard from insider this could be the next BAYC 👀 NFA DYOR',
            'created_at': datetime.now() - timedelta(hours=16),
            'author_id': 'user8',
            'like_count': 78,
            'retweet_count': 29,
            'reply_count': 12,
            'quote_count': 4
        },
        {
            'id': '9',
            'text': '$DOGE to the moon! 🌙 Elon tweeted again and the community is going crazy. Diamond hands!',
            'created_at': datetime.now() - timedelta(hours=18),
            'author_id': 'user9',
            'like_count': 234,
            'retweet_count': 123,
            'reply_count': 67,
            'quote_count': 23
        },
        {
            'id': '10',
            'text': 'Technical analysis: $BTC forming a bull flag on the 4h chart. Target $50k if we break resistance',
            'created_at': datetime.now() - timedelta(hours=20),
            'author_id': 'user10',
            'like_count': 156,
            'retweet_count': 67,
            'reply_count': 34,
            'quote_count': 11
        }
    ]
    
    return demo_tweets

def run_demo():
    """Run the demo analysis"""
    print("🚀 Crypto X Analyzer Demo")
    print("=" * 50)
    
    # Generate demo data
    print("📊 Generating demo tweets...")
    tweets = generate_demo_tweets()
    
    # Initialize services
    print("🔧 Initializing analytics...")
    analytics_service = AnalyticsService()
    ticker_extractor = TickerExtractor()
    
    # Run analysis
    print("🔍 Analyzing tweets...")
    analysis = analytics_service.analyze_feed_summary(tweets, 'demo')
    
    # Display results
    print("\n" + "=" * 50)
    print("📈 ANALYSIS RESULTS")
    print("=" * 50)
    
    # Summary
    summary = analysis['summary']
    print(f"📊 Total Tweets: {summary['total_tweets']}")
    print(f"👥 Unique Authors: {summary['unique_authors']}")
    
    # Key insights
    print(f"\n🎯 KEY INSIGHTS:")
    for insight in analysis['key_insights']:
        print(f"   • {insight}")
    
    # Top tickers
    print(f"\n🪙 TOP MENTIONED TICKERS:")
    for ticker in analysis['ticker_analysis']['top_tickers'][:5]:
        symbol = ticker['symbol']
        mentions = ticker['mentions']
        sentiment_data = analysis['ticker_analysis']['ticker_sentiment'].get(symbol, {})
        bullish_ratio = sentiment_data.get('bullish_ratio', 0) * 100
        print(f"   ${symbol}: {mentions} mentions ({bullish_ratio:.1f}% bullish)")
    
    # Sentiment
    sentiment = analysis['sentiment_analysis']
    print(f"\n😊 SENTIMENT ANALYSIS:")
    print(f"   Overall: {sentiment['overall_sentiment'].title()}")
    print(f"   Crypto-specific: {sentiment['crypto_sentiment'].title()}")
    
    # Alpha signals
    alpha = analysis['alpha_signals']
    print(f"\n🚨 ALPHA SIGNALS:")
    print(f"   Alpha signals detected: {alpha['alpha_signal_count']}")
    print(f"   Warning signals: {alpha['warning_signal_count']}")
    print(f"   Risk/Reward ratio: {alpha['risk_reward_ratio']:.2f}")
    
    # Top themes
    themes = analysis['themes']
    if themes['top_themes']:
        print(f"\n🏷️ TOP THEMES:")
        for theme, data in list(themes['top_themes'].items())[:3]:
            print(f"   {theme.title()}: {data['mentions']} mentions ({data['sentiment_label']})")
    
    # Engagement
    engagement = analysis['engagement_analysis']
    print(f"\n💬 ENGAGEMENT:")
    print(f"   Total engagement: {engagement['total_engagement']:,}")
    print(f"   Average per tweet: {engagement['average_engagement']:.1f}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed!")
    print("🔗 To use with real data, configure your Twitter API keys in .env")
    print("🚀 Run 'streamlit run app.py' to start the full application")

if __name__ == "__main__":
    run_demo()