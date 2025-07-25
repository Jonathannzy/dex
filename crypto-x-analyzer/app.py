import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

from services.twitter_service import TwitterService
from services.analytics_service import AnalyticsService
from config import Config

# Set page config
st.set_page_config(
    page_title="Crypto X Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize services
@st.cache_resource
def init_services():
    return TwitterService(), AnalyticsService()

def main():
    st.title("🚀 Crypto X (Twitter) Analyzer")
    st.markdown("**Find Alpha in the Crypto Twitter Sphere**")
    
    # Check if API keys are configured
    if not check_api_configuration():
        show_api_configuration_help()
        return
    
    twitter_service, analytics_service = init_services()
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Analysis timeframe
        timeframe = st.selectbox(
            "Analysis Timeframe",
            options=["short", "medium", "long"],
            format_func=lambda x: f"{x.title()} ({Config.ANALYSIS_TIMEFRAMES[x]} days)",
            index=1
        )
        
        # Data source selection
        data_source = st.radio(
            "Data Source",
            ["Your Feed", "Search Crypto Tweets", "Specific Account"],
            help="Choose what data to analyze"
        )
        
        # Additional options based on data source
        username = None
        if data_source == "Specific Account":
            username = st.text_input("Username (without @)", placeholder="elonmusk")
        
        max_tweets = st.slider("Max Tweets to Analyze", 100, 2000, 500, 100)
        
        # Analysis button
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    # Main content area
    if analyze_button:
        with st.spinner("Fetching and analyzing data..."):
            # Fetch data based on selection
            tweets = fetch_tweets(twitter_service, data_source, timeframe, username, max_tweets)
            
            if not tweets:
                st.error("No tweets found. Please check your configuration and try again.")
                return
            
            # Analyze the data
            analysis = analytics_service.analyze_feed_summary(tweets, timeframe)
            
            # Display results
            display_analysis_results(analysis, analytics_service)
    
    else:
        # Show welcome screen
        show_welcome_screen()

def check_api_configuration():
    """Check if required API keys are configured"""
    return bool(Config.TWITTER_BEARER_TOKEN or 
               (Config.TWITTER_API_KEY and Config.TWITTER_API_SECRET))

def show_api_configuration_help():
    """Show help for API configuration"""
    st.error("🔑 API Configuration Required")
    st.markdown("""
    To use this app, you need to configure your Twitter API credentials. 
    
    **Required API Keys:**
    - Twitter Bearer Token (recommended) OR
    - Twitter API Key + API Secret + Access Token + Access Token Secret
    
    **Setup Instructions:**
    1. Create a `.env` file in the crypto-x-analyzer directory
    2. Add your API credentials:
    
    ```
    # Twitter API v2 (Recommended)
    TWITTER_BEARER_TOKEN=your_bearer_token_here
    
    # OR Twitter API v1.1
    TWITTER_API_KEY=your_api_key
    TWITTER_API_SECRET=your_api_secret
    TWITTER_ACCESS_TOKEN=your_access_token
    TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
    
    # Optional: For enhanced analysis
    OPENAI_API_KEY=your_openai_key
    CMC_API_KEY=your_coinmarketcap_key
    ```
    
    **Get Twitter API Access:**
    1. Go to [developer.twitter.com](https://developer.twitter.com)
    2. Apply for a developer account
    3. Create a new app and get your credentials
    """)

def fetch_tweets(twitter_service, data_source, timeframe, username, max_tweets):
    """Fetch tweets based on user selection"""
    days = Config.ANALYSIS_TIMEFRAMES[timeframe]
    
    if data_source == "Your Feed":
        return twitter_service.get_user_feed(username or "user", days=days, max_tweets=max_tweets)
    elif data_source == "Search Crypto Tweets":
        return twitter_service.search_crypto_tweets(days=days, max_tweets=max_tweets)
    elif data_source == "Specific Account" and username:
        return twitter_service.get_user_timeline(username, days=days, max_tweets=max_tweets)
    
    return []

def display_analysis_results(analysis, analytics_service):
    """Display the comprehensive analysis results"""
    
    # Key metrics at the top
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tweets", analysis['summary']['total_tweets'])
    with col2:
        st.metric("Unique Authors", analysis['summary']['unique_authors'])
    with col3:
        sentiment = analysis['sentiment_analysis']['crypto_sentiment']
        sentiment_color = "🟢" if sentiment == "bullish" else "🔴" if sentiment == "bearish" else "🟡"
        st.metric("Crypto Sentiment", f"{sentiment_color} {sentiment.title()}")
    with col4:
        alpha_signals = analysis['alpha_signals']['alpha_signal_count']
        st.metric("Alpha Signals", alpha_signals)
    
    # Key insights
    st.header("🎯 Key Insights")
    for insight in analysis['key_insights']:
        st.success(insight)
    
    # Create tabs for different analysis sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Ticker Analysis", 
        "🎭 Sentiment & Themes", 
        "🚨 Alpha Signals", 
        "⚡ Engagement", 
        "👥 Account Recommendations"
    ])
    
    with tab1:
        display_ticker_analysis(analysis['ticker_analysis'])
    
    with tab2:
        display_sentiment_and_themes(analysis['sentiment_analysis'], analysis['themes'])
    
    with tab3:
        display_alpha_signals(analysis['alpha_signals'])
    
    with tab4:
        display_engagement_analysis(analysis['engagement_analysis'], analysis['temporal_analysis'])
    
    with tab5:
        display_account_recommendations(analytics_service)

def display_ticker_analysis(ticker_analysis):
    """Display ticker analysis section"""
    st.subheader("🪙 Most Mentioned Tickers")
    
    if ticker_analysis['top_tickers']:
        # Create a chart of top tickers
        ticker_df = pd.DataFrame(ticker_analysis['top_tickers'][:10])
        
        fig = px.bar(
            ticker_df, 
            x='symbol', 
            y='mentions',
            title="Top Cryptocurrency Mentions",
            color='mentions',
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display ticker sentiment table
        st.subheader("📊 Ticker Sentiment Analysis")
        
        sentiment_data = []
        for ticker in ticker_analysis['top_tickers'][:10]:
            symbol = ticker['symbol']
            sentiment_info = ticker_analysis['ticker_sentiment'].get(symbol, {})
            
            sentiment_data.append({
                'Ticker': f"${symbol}",
                'Mentions': ticker['mentions'],
                'Bullish %': f"{sentiment_info.get('bullish_ratio', 0)*100:.1f}%",
                'Bearish %': f"{sentiment_info.get('bearish_ratio', 0)*100:.1f}%",
                'Neutral %': f"{sentiment_info.get('neutral_ratio', 0)*100:.1f}%",
                'Confidence': f"{sentiment_info.get('avg_confidence', 0):.2f}"
            })
        
        st.dataframe(sentiment_data, use_container_width=True)
    else:
        st.info("No ticker mentions found in the analyzed tweets.")
    
    # Trending tickers
    if ticker_analysis.get('trending_tickers'):
        st.subheader("🔥 Trending Tickers")
        for ticker in ticker_analysis['trending_tickers'][:5]:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**${ticker['symbol']}**")
            with col2:
                st.write(f"{ticker['mentions']} mentions")
            with col3:
                st.write(f"Trend Score: {ticker['trend_score']:.1f}")

def display_sentiment_and_themes(sentiment_analysis, themes):
    """Display sentiment and themes analysis"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("😊 Sentiment Distribution")
        
        # Sentiment pie chart
        sentiment_dist = sentiment_analysis['sentiment_distribution']
        fig = px.pie(
            values=[sentiment_dist['bullish'], sentiment_dist['neutral'], sentiment_dist['bearish']],
            names=['Bullish', 'Neutral', 'Bearish'],
            title="Overall Sentiment Distribution",
            color_discrete_map={'Bullish': '#00ff00', 'Neutral': '#ffff00', 'Bearish': '#ff0000'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏷️ Top Themes")
        
        if themes['top_themes']:
            theme_data = []
            for theme, data in themes['top_themes'].items():
                theme_data.append({
                    'Theme': theme.title(),
                    'Mentions': data['mentions'],
                    'Sentiment': data['sentiment_label'].title(),
                    'Score': f"{data['avg_sentiment']:.2f}"
                })
            
            st.dataframe(theme_data, use_container_width=True)
        else:
            st.info("No themes detected.")
    
    # Detailed sentiment metrics
    st.subheader("📈 Sentiment Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Sentiment", sentiment_analysis['overall_sentiment'].title())
    with col2:
        st.metric("Crypto Sentiment", sentiment_analysis['crypto_sentiment'].title())
    with col3:
        st.metric("Overall Score", f"{sentiment_analysis['overall_score']:.3f}")
    with col4:
        st.metric("Crypto Score", f"{sentiment_analysis['crypto_score']:.3f}")

def display_alpha_signals(alpha_signals):
    """Display alpha signals section"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Alpha Signals Detected")
        
        if alpha_signals['alpha_signals']:
            for i, signal in enumerate(alpha_signals['alpha_signals'][:5], 1):
                with st.expander(f"Signal #{i}: {signal['keyword'].upper()}"):
                    st.write(f"**Tweet:** {signal['text']}")
                    st.write(f"**Engagement:** {signal['engagement']} interactions")
                    if signal['tickers']:
                        st.write(f"**Mentioned Tickers:** {', '.join(['$' + t for t in signal['tickers']])}")
        else:
            st.info("No alpha signals detected in the current timeframe.")
    
    with col2:
        st.subheader("⚠️ Warning Signals")
        
        if alpha_signals['warning_signals']:
            for signal in alpha_signals['warning_signals'][:3]:
                st.warning(f"**{signal['keyword'].upper()}**: {signal['text'][:100]}...")
        else:
            st.success("No warning signals detected.")
        
        # Risk/Reward ratio
        st.metric("Risk/Reward Ratio", f"{alpha_signals['risk_reward_ratio']:.2f}")

def display_engagement_analysis(engagement_analysis, temporal_analysis):
    """Display engagement and temporal analysis"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💬 Engagement Metrics")
        
        st.metric("Total Engagement", f"{engagement_analysis.get('total_engagement', 0):,}")
        st.metric("Average Engagement", f"{engagement_analysis.get('average_engagement', 0):.1f}")
        st.metric("Median Engagement", f"{engagement_analysis.get('median_engagement', 0):.1f}")
    
    with col2:
        st.subheader("⏰ Temporal Patterns")
        
        if 'peak_hour' in temporal_analysis:
            st.metric("Peak Hour", f"{temporal_analysis['peak_hour']}:00")
            st.metric("Peak Day", temporal_analysis['peak_day'])
            st.metric("Recent Trend", temporal_analysis['recent_trend'].title())
    
    # Top performing tweets
    if engagement_analysis.get('top_performing_tweets'):
        st.subheader("🏆 Top Performing Tweets")
        
        for i, tweet in enumerate(engagement_analysis['top_performing_tweets'], 1):
            with st.expander(f"Tweet #{i} - {tweet['engagement']} interactions"):
                st.write(tweet['text'])
                st.write(f"👍 {tweet['likes']} likes | 🔄 {tweet['retweets']} retweets")

def display_account_recommendations(analytics_service):
    """Display account recommendations"""
    st.subheader("👥 Recommended Crypto Accounts to Follow")
    
    with st.spinner("Analyzing crypto accounts..."):
        try:
            recommendations = analytics_service.generate_account_recommendations()
            
            if recommendations:
                for i, account in enumerate(recommendations[:10], 1):
                    with st.expander(f"{i}. @{account['username']} {account['name']}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**Crypto Focus:** {account['crypto_focus']:.1%}")
                            if account['verified']:
                                st.write("✅ Verified")
                        
                        with col2:
                            st.write(f"**Avg Engagement:** {account['avg_engagement']:.1f}")
                            st.write(f"**Score:** {account['recommendation_score']:.1f}")
                        
                        with col3:
                            st.write(account['reason'])
                        
                        st.write(f"*{account['analysis']}*")
            else:
                st.info("Unable to generate recommendations at this time.")
        
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")

def show_welcome_screen():
    """Show welcome screen with instructions"""
    st.markdown("""
    ## Welcome to Crypto X Analyzer! 🚀
    
    This tool helps you find alpha in the crypto Twitter sphere by analyzing:
    
    ### 📊 What We Analyze:
    - **Ticker Mentions**: Extract and track cryptocurrency mentions
    - **Sentiment Analysis**: Gauge market sentiment for different coins
    - **Alpha Signals**: Detect early opportunities and hidden gems
    - **Trending Topics**: Identify what's hot in crypto right now
    - **Account Recommendations**: Find the best crypto accounts to follow
    - **Engagement Patterns**: See what content performs best
    
    ### 🎯 Perfect For:
    - Finding early altcoin opportunities
    - Tracking sentiment around your portfolio
    - Discovering influential crypto accounts
    - Identifying market trends before they explode
    
    ### 🚀 Get Started:
    1. Configure your settings in the sidebar
    2. Choose your data source
    3. Click "Analyze" to start finding alpha!
    
    ---
    
    ⚠️ **Disclaimer**: This tool is for informational purposes only. Always do your own research (DYOR) before making investment decisions.
    """)

if __name__ == "__main__":
    main()