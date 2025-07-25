import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # X (Twitter) API credentials
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    # CoinMarketCap API
    CMC_API_KEY = os.getenv('CMC_API_KEY')
    
    # OpenAI API (for enhanced analysis)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Anthropic API (alternative to OpenAI)
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    
    # Database configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///crypto_analyzer.db')
    
    # Redis configuration (for caching)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # Analysis settings
    MAX_TWEETS_PER_REQUEST = 100
    TWEET_ANALYSIS_BATCH_SIZE = 50
    CRYPTO_KEYWORDS = [
        'bitcoin', 'btc', 'ethereum', 'eth', 'altcoin', 'altcoins', 'defi', 'nft',
        'crypto', 'cryptocurrency', 'blockchain', 'hodl', 'pump', 'dump', 'moon',
        'lambo', 'diamond hands', 'paper hands', 'whale', 'ape', 'degen', 'alpha',
        'beta', 'gamma', 'farming', 'yield', 'staking', 'liquidity', 'airdrop',
        'tokenomics', 'web3', 'metaverse', 'dao', 'dex', 'cex', 'cefi', 'gamefi'
    ]
    
    # Top crypto accounts to analyze for recommendations
    TOP_CRYPTO_ACCOUNTS = [
        'elonmusk', 'VitalikButerin', 'cz_binance', 'aantonop', 'naval',
        'APompliano', 'Michael_Saylor', 'RaoulGMI', 'DocumentingBTC',
        '100trillionUSD', 'BitcoinMagazine', 'Cointelegraph', 'CoinDesk',
        'defipulse', 'DeFiPulse', 'TheBlock__', 'Messari', 'santimentfeed',
        'whale_alert', 'lookonchain', 'ai_9684xtpa', 'EmberCN', 'spotonchain'
    ]
    
    # Timeframes for analysis
    ANALYSIS_TIMEFRAMES = {
        'short': 1,   # 1 day
        'medium': 7,  # 1 week
        'long': 30    # 1 month
    }