# 🚀 Crypto X (Twitter) Analyzer

Find Alpha in the Crypto Twitter Sphere! This application analyzes your X (Twitter) data to identify cryptocurrency opportunities, track sentiment, and recommend the best crypto accounts to follow.

## 🎯 Features

### 📊 Feed Analysis
- **Ticker Extraction**: Automatically detect cryptocurrency mentions ($BTC, $ETH, etc.)
- **Sentiment Analysis**: Gauge bullish/bearish sentiment for specific coins
- **Alpha Signal Detection**: Identify early opportunities and hidden gems
- **Trending Analysis**: Track what's hot in crypto right now

### 🔍 Account Intelligence
- **Account Recommendations**: Discover the best crypto accounts to follow
- **Crypto Focus Analysis**: Evaluate how crypto-focused an account is
- **Engagement Metrics**: Track which content performs best

### 📈 Market Insights
- **Price Target Extraction**: Extract price predictions from tweets
- **Theme Analysis**: Identify trending topics (DeFi, NFTs, altcoins, etc.)
- **Temporal Patterns**: Understand when crypto content is most active
- **Warning Signals**: Detect potential scams or risky situations

## 🛠️ Installation

1. **Clone or download the application**
   ```bash
   cd crypto-x-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔑 API Setup

### Twitter API (Required)
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Apply for a developer account
3. Create a new app
4. Get your Bearer Token (recommended) or API keys

### Optional APIs
- **CoinMarketCap**: For enhanced crypto data
- **OpenAI**: For advanced text analysis
- **Anthropic**: Alternative AI analysis

## 📋 Usage

### Quick Start
1. Open the app in your browser
2. Configure your API credentials in `.env`
3. Choose your analysis settings:
   - **Your Feed**: Analyze your Twitter timeline
   - **Search Crypto Tweets**: Analyze recent crypto discussions
   - **Specific Account**: Analyze a particular user's tweets
4. Click "Analyze" and discover alpha!

### Analysis Options

#### Timeframes
- **Short (1 day)**: Latest trends and immediate opportunities
- **Medium (7 days)**: Weekly patterns and emerging trends
- **Long (30 days)**: Long-term sentiment and established trends

#### Data Sources
- **Your Feed**: Personal timeline analysis (requires authentication)
- **Search Crypto Tweets**: Public crypto discussions
- **Specific Account**: Individual account analysis

## 📊 What You'll Discover

### 🪙 Ticker Analysis
- Most mentioned cryptocurrencies
- Sentiment breakdown per ticker
- Trending coins with momentum scores
- Price targets and predictions

### 🎭 Sentiment & Themes
- Overall market sentiment
- Topic analysis (DeFi, NFTs, trading, etc.)
- Sentiment distribution charts
- Theme-specific sentiment

### 🚨 Alpha Signals
- Early opportunity detection
- Hidden gem identification
- Warning signal alerts
- Risk/reward ratios

### 👥 Account Recommendations
- Top crypto influencers to follow
- Engagement-based rankings
- Crypto focus analysis
- Verified account prioritization

## 🎯 Perfect For

- **Crypto Traders**: Find early altcoin opportunities
- **Investors**: Track sentiment around your portfolio
- **Researchers**: Analyze market trends and patterns
- **Content Creators**: Understand what resonates in crypto Twitter

## ⚠️ Important Notes

### Rate Limits
- Twitter API has rate limits
- Free tier: Limited requests per 15 minutes
- Paid tier: Higher limits available

### Data Quality
- Analysis quality depends on data volume
- More tweets = better insights
- Consider multiple timeframes for comprehensive analysis

### Investment Disclaimer
**This tool is for informational purposes only. Always do your own research (DYOR) before making investment decisions. Cryptocurrency investments carry significant risk.**

## 🔧 Troubleshooting

### Common Issues

1. **"No tweets found"**
   - Check your API credentials
   - Verify account username (without @)
   - Try different timeframes
   - Check Twitter API rate limits

2. **"API Configuration Required"**
   - Ensure `.env` file exists
   - Verify API keys are correct
   - Check API key permissions

3. **Low-quality results**
   - Increase tweet count
   - Try longer timeframes
   - Use multiple data sources

### Rate Limit Solutions
- Use longer analysis intervals
- Reduce max tweet count
- Consider Twitter API Pro for higher limits

## 📈 Advanced Features

### Custom Analysis
- Modify ticker lists in `config.py`
- Adjust sentiment keywords
- Configure alpha signal detection

### Data Export
- Analysis results are in JSON format
- Easy to export to CSV/Excel
- API integration friendly

### Scalability
- SQLite database for data storage
- Redis caching support
- Designed for high-volume analysis

## 🤝 Contributing

This is an open framework for crypto Twitter analysis. Feel free to:
- Add new analysis features
- Improve sentiment detection
- Enhance ticker extraction
- Add new data sources

## 📚 Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Backend**: Python services
- **Data**: Twitter API integration
- **Analysis**: NLP and sentiment analysis
- **Storage**: SQLite/PostgreSQL support

### Key Components
- `services/twitter_service.py`: Twitter API integration
- `services/analytics_service.py`: Analysis engine
- `utils/ticker_extractor.py`: Cryptocurrency detection
- `app.py`: Streamlit interface
- `config.py`: Configuration management

### Dependencies
- `tweepy`: Twitter API client
- `streamlit`: Web interface
- `pandas`: Data manipulation
- `plotly`: Interactive charts
- `textblob`: Sentiment analysis
- `nltk`: Natural language processing

## 🚀 Getting Started

Ready to find alpha in crypto Twitter? 

1. Set up your API credentials
2. Run the app
3. Start analyzing!

Remember: The best alpha comes from combining multiple signals and doing your own research. This tool helps you identify opportunities, but always verify before investing.

Happy hunting! 🎯