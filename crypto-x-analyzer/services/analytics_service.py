import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from collections import Counter, defaultdict
import logging
from textblob import TextBlob
import re

from utils.ticker_extractor import TickerExtractor
from services.twitter_service import TwitterService

class AnalyticsService:
    def __init__(self):
        self.ticker_extractor = TickerExtractor()
        self.twitter_service = TwitterService()
        self.logger = logging.getLogger(__name__)
        
    def analyze_feed_summary(self, tweets: List[Dict], timeframe: str = 'medium') -> Dict:
        """Generate comprehensive feed summary with crypto insights"""
        if not tweets:
            return self._empty_summary()
        
        df = pd.DataFrame(tweets)
        
        # Basic metrics
        total_tweets = len(tweets)
        unique_authors = df['author_id'].nunique() if 'author_id' in df.columns else 0
        
        # Time analysis
        time_analysis = self._analyze_temporal_patterns(df)
        
        # Ticker extraction and analysis
        ticker_analysis = self._analyze_tickers_in_tweets(tweets)
        
        # Sentiment analysis
        sentiment_analysis = self._analyze_sentiment(tweets)
        
        # Engagement analysis
        engagement_analysis = self._analyze_engagement(df)
        
        # Alpha signals detection
        alpha_signals = self._detect_alpha_signals(tweets)
        
        # Top themes and topics
        themes = self._extract_themes(tweets)
        
        return {
            'summary': {
                'total_tweets': total_tweets,
                'unique_authors': unique_authors,
                'timeframe': timeframe,
                'analysis_date': datetime.now().isoformat(),
            },
            'temporal_analysis': time_analysis,
            'ticker_analysis': ticker_analysis,
            'sentiment_analysis': sentiment_analysis,
            'engagement_analysis': engagement_analysis,
            'alpha_signals': alpha_signals,
            'themes': themes,
            'key_insights': self._generate_key_insights(ticker_analysis, sentiment_analysis, alpha_signals)
        }
    
    def _analyze_temporal_patterns(self, df: pd.DataFrame) -> Dict:
        """Analyze when crypto content is posted"""
        if 'created_at' not in df.columns or df['created_at'].isna().all():
            return {'pattern': 'No temporal data available'}
        
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['hour'] = df['created_at'].dt.hour
        df['day_of_week'] = df['created_at'].dt.day_name()
        
        # Peak hours
        hourly_counts = df['hour'].value_counts().sort_index()
        peak_hour = hourly_counts.idxmax()
        
        # Peak days
        daily_counts = df['day_of_week'].value_counts()
        peak_day = daily_counts.idxmax()
        
        # Recent activity trend (last 24h vs previous 24h)
        now = datetime.now()
        last_24h = df[df['created_at'] >= now - timedelta(hours=24)]
        prev_24h = df[(df['created_at'] >= now - timedelta(hours=48)) & 
                      (df['created_at'] < now - timedelta(hours=24))]
        
        trend = 'stable'
        if len(last_24h) > len(prev_24h) * 1.2:
            trend = 'increasing'
        elif len(last_24h) < len(prev_24h) * 0.8:
            trend = 'decreasing'
        
        return {
            'peak_hour': int(peak_hour),
            'peak_day': peak_day,
            'hourly_distribution': hourly_counts.to_dict(),
            'daily_distribution': daily_counts.to_dict(),
            'recent_trend': trend,
            'tweets_last_24h': len(last_24h),
            'tweets_prev_24h': len(prev_24h)
        }
    
    def _analyze_tickers_in_tweets(self, tweets: List[Dict]) -> Dict:
        """Extract and analyze cryptocurrency tickers from tweets"""
        all_tickers = []
        ticker_contexts = defaultdict(list)
        ticker_sentiments = defaultdict(list)
        ticker_prices = defaultdict(list)
        
        for tweet in tweets:
            text = tweet.get('text', '')
            tickers = self.ticker_extractor.extract_tickers_from_text(text)
            
            for ticker_data in tickers:
                symbol = ticker_data['symbol']
                context = ticker_data['context']
                
                all_tickers.append(symbol)
                ticker_contexts[symbol].append(context)
                
                # Analyze sentiment for this ticker mention
                sentiment = self.ticker_extractor.analyze_sentiment_context(context)
                ticker_sentiments[symbol].append(sentiment)
                
                # Extract price targets
                prices = self.ticker_extractor.extract_price_targets(context)
                if prices:
                    ticker_prices[symbol].extend(prices)
        
        # Count ticker mentions
        ticker_counts = Counter(all_tickers)
        
        # Aggregate sentiment by ticker
        ticker_sentiment_summary = {}
        for symbol, sentiments in ticker_sentiments.items():
            bullish = sum(1 for s in sentiments if s['sentiment'] == 'bullish')
            bearish = sum(1 for s in sentiments if s['sentiment'] == 'bearish')
            neutral = len(sentiments) - bullish - bearish
            
            total = len(sentiments)
            ticker_sentiment_summary[symbol] = {
                'bullish_ratio': bullish / total if total > 0 else 0,
                'bearish_ratio': bearish / total if total > 0 else 0,
                'neutral_ratio': neutral / total if total > 0 else 0,
                'total_mentions': total,
                'avg_confidence': np.mean([s['confidence'] for s in sentiments]) if sentiments else 0
            }
        
        # Top mentioned tickers
        top_tickers = ticker_counts.most_common(20)
        
        return {
            'total_ticker_mentions': len(all_tickers),
            'unique_tickers': len(ticker_counts),
            'top_tickers': [{'symbol': symbol, 'mentions': count} for symbol, count in top_tickers],
            'ticker_sentiment': ticker_sentiment_summary,
            'ticker_price_targets': dict(ticker_prices),
            'trending_tickers': self._identify_trending_tickers(ticker_counts, ticker_sentiment_summary)
        }
    
    def _analyze_sentiment(self, tweets: List[Dict]) -> Dict:
        """Analyze overall sentiment of the feed"""
        sentiments = []
        crypto_sentiments = []
        
        for tweet in tweets:
            text = tweet.get('text', '')
            
            # Overall sentiment
            blob = TextBlob(text)
            sentiment_score = blob.sentiment.polarity
            sentiments.append(sentiment_score)
            
            # Crypto-specific sentiment
            if any(keyword in text.lower() for keyword in ['crypto', 'bitcoin', 'ethereum', '$']):
                crypto_sentiments.append(sentiment_score)
        
        overall_sentiment = np.mean(sentiments) if sentiments else 0
        crypto_sentiment = np.mean(crypto_sentiments) if crypto_sentiments else 0
        
        # Classify sentiment
        def classify_sentiment(score):
            if score > 0.1:
                return 'bullish'
            elif score < -0.1:
                return 'bearish'
            else:
                return 'neutral'
        
        return {
            'overall_sentiment': classify_sentiment(overall_sentiment),
            'overall_score': overall_sentiment,
            'crypto_sentiment': classify_sentiment(crypto_sentiment),
            'crypto_score': crypto_sentiment,
            'sentiment_distribution': {
                'bullish': sum(1 for s in sentiments if s > 0.1),
                'bearish': sum(1 for s in sentiments if s < -0.1),
                'neutral': sum(1 for s in sentiments if -0.1 <= s <= 0.1)
            },
            'total_analyzed': len(sentiments)
        }
    
    def _analyze_engagement(self, df: pd.DataFrame) -> Dict:
        """Analyze engagement patterns"""
        if df.empty:
            return {'total_engagement': 0}
        
        # Calculate engagement metrics
        engagement_cols = ['like_count', 'retweet_count', 'reply_count', 'quote_count']
        available_cols = [col for col in engagement_cols if col in df.columns]
        
        if not available_cols:
            return {'total_engagement': 0, 'note': 'No engagement data available'}
        
        df['total_engagement'] = df[available_cols].sum(axis=1)
        
        total_engagement = df['total_engagement'].sum()
        avg_engagement = df['total_engagement'].mean()
        top_tweets = df.nlargest(5, 'total_engagement')
        
        return {
            'total_engagement': int(total_engagement),
            'average_engagement': float(avg_engagement),
            'median_engagement': float(df['total_engagement'].median()),
            'top_performing_tweets': [
                {
                    'text': row.get('text', '')[:100] + '...' if len(row.get('text', '')) > 100 else row.get('text', ''),
                    'engagement': int(row['total_engagement']),
                    'likes': int(row.get('like_count', 0)),
                    'retweets': int(row.get('retweet_count', 0))
                }
                for _, row in top_tweets.iterrows()
            ][:3]
        }
    
    def _detect_alpha_signals(self, tweets: List[Dict]) -> Dict:
        """Detect potential alpha signals in the feed"""
        alpha_keywords = [
            'gem', 'alpha', 'early', 'hidden', 'under radar', 'undervalued',
            'presale', 'ido', 'ico', 'launch', 'fair launch', 'stealth launch',
            'low cap', 'microcap', 'moonshot', '100x', '10x', 'next big thing',
            'dyor', 'nfa', 'ape', 'yolo', 'insider', 'whale accumulation'
        ]
        
        warning_keywords = [
            'rug', 'scam', 'ponzi', 'honeypot', 'exit scam', 'dump incoming',
            'avoid', 'warning', 'be careful', 'sus', 'suspicious'
        ]
        
        alpha_signals = []
        warning_signals = []
        
        for tweet in tweets:
            text = tweet.get('text', '').lower()
            
            # Check for alpha signals
            for keyword in alpha_keywords:
                if keyword in text:
                    tickers = self.ticker_extractor.extract_tickers_from_text(tweet.get('text', ''))
                    alpha_signals.append({
                        'keyword': keyword,
                        'text': tweet.get('text', '')[:200],
                        'engagement': tweet.get('like_count', 0) + tweet.get('retweet_count', 0),
                        'tickers': [t['symbol'] for t in tickers],
                        'created_at': tweet.get('created_at')
                    })
                    break
            
            # Check for warning signals
            for keyword in warning_keywords:
                if keyword in text:
                    tickers = self.ticker_extractor.extract_tickers_from_text(tweet.get('text', ''))
                    warning_signals.append({
                        'keyword': keyword,
                        'text': tweet.get('text', '')[:200],
                        'tickers': [t['symbol'] for t in tickers],
                        'created_at': tweet.get('created_at')
                    })
                    break
        
        # Sort by engagement for alpha signals
        alpha_signals.sort(key=lambda x: x['engagement'], reverse=True)
        
        return {
            'alpha_signals': alpha_signals[:10],
            'warning_signals': warning_signals[:5],
            'alpha_signal_count': len(alpha_signals),
            'warning_signal_count': len(warning_signals),
            'risk_reward_ratio': len(alpha_signals) / max(len(warning_signals), 1)
        }
    
    def _extract_themes(self, tweets: List[Dict]) -> Dict:
        """Extract main themes and topics from tweets"""
        themes = {
            'defi': ['defi', 'decentralized finance', 'yield farming', 'liquidity', 'staking', 'dex'],
            'nft': ['nft', 'non-fungible', 'opensea', 'collectible', 'art', 'pfp'],
            'altcoins': ['altcoin', 'alt', 'altseason', 'altcoin season'],
            'bitcoin': ['bitcoin', 'btc', 'digital gold', 'store of value'],
            'ethereum': ['ethereum', 'eth', 'gas fees', 'erc-20'],
            'memecoins': ['meme', 'dogecoin', 'shiba', 'pepe', 'frog'],
            'trading': ['trading', 'pump', 'dump', 'chart', 'technical analysis', 'ta'],
            'web3': ['web3', 'metaverse', 'dao', 'decentralization'],
            'regulation': ['regulation', 'sec', 'etf', 'government', 'legal']
        }
        
        theme_counts = {theme: 0 for theme in themes}
        theme_sentiment = {theme: [] for theme in themes}
        
        for tweet in tweets:
            text = tweet.get('text', '').lower()
            
            for theme, keywords in themes.items():
                if any(keyword in text for keyword in keywords):
                    theme_counts[theme] += 1
                    
                    # Analyze sentiment for this theme
                    blob = TextBlob(tweet.get('text', ''))
                    theme_sentiment[theme].append(blob.sentiment.polarity)
        
        # Calculate average sentiment by theme
        theme_analysis = {}
        for theme, count in theme_counts.items():
            if count > 0:
                avg_sentiment = np.mean(theme_sentiment[theme])
                theme_analysis[theme] = {
                    'mentions': count,
                    'avg_sentiment': avg_sentiment,
                    'sentiment_label': 'bullish' if avg_sentiment > 0.1 else 'bearish' if avg_sentiment < -0.1 else 'neutral'
                }
        
        # Sort themes by mentions
        sorted_themes = sorted(theme_analysis.items(), key=lambda x: x[1]['mentions'], reverse=True)
        
        return {
            'top_themes': dict(sorted_themes[:5]),
            'all_themes': theme_analysis,
            'dominant_theme': sorted_themes[0][0] if sorted_themes else None
        }
    
    def _identify_trending_tickers(self, ticker_counts: Counter, sentiment_summary: Dict) -> List[Dict]:
        """Identify trending tickers based on mentions and sentiment"""
        trending = []
        
        for symbol, count in ticker_counts.most_common(10):
            sentiment_data = sentiment_summary.get(symbol, {})
            
            # Calculate trend score (mentions * bullish ratio)
            bullish_ratio = sentiment_data.get('bullish_ratio', 0)
            trend_score = count * (1 + bullish_ratio)
            
            trending.append({
                'symbol': symbol,
                'mentions': count,
                'bullish_ratio': bullish_ratio,
                'trend_score': trend_score,
                'confidence': sentiment_data.get('avg_confidence', 0)
            })
        
        # Sort by trend score
        trending.sort(key=lambda x: x['trend_score'], reverse=True)
        return trending[:5]
    
    def _generate_key_insights(self, ticker_analysis: Dict, sentiment_analysis: Dict, alpha_signals: Dict) -> List[str]:
        """Generate key actionable insights"""
        insights = []
        
        # Top ticker insight
        if ticker_analysis['top_tickers']:
            top_ticker = ticker_analysis['top_tickers'][0]
            insights.append(f"Most discussed: ${top_ticker['symbol']} ({top_ticker['mentions']} mentions)")
        
        # Sentiment insight
        crypto_sentiment = sentiment_analysis['crypto_sentiment']
        insights.append(f"Overall crypto sentiment: {crypto_sentiment}")
        
        # Alpha signal insight
        alpha_count = alpha_signals['alpha_signal_count']
        if alpha_count > 0:
            insights.append(f"Detected {alpha_count} potential alpha signals - investigate for opportunities")
        
        # Warning insight
        warning_count = alpha_signals['warning_signal_count']
        if warning_count > 0:
            insights.append(f"⚠️ {warning_count} warning signals detected - exercise caution")
        
        # Trending ticker insight
        if ticker_analysis.get('trending_tickers'):
            trending = ticker_analysis['trending_tickers'][0]
            insights.append(f"Trending: ${trending['symbol']} (trend score: {trending['trend_score']:.1f})")
        
        return insights
    
    def _empty_summary(self) -> Dict:
        """Return empty summary when no data is available"""
        return {
            'summary': {'total_tweets': 0, 'unique_authors': 0},
            'message': 'No data available for analysis'
        }
    
    def generate_account_recommendations(self, current_following: List[str] = None) -> List[Dict]:
        """Generate recommended crypto accounts to follow"""
        if current_following is None:
            current_following = []
        
        # Analyze trending accounts
        trending_accounts = self.twitter_service.get_trending_crypto_accounts(limit=100)
        
        recommendations = []
        for account in trending_accounts:
            # Skip if already following
            if account['username'] in current_following:
                continue
            
            # Analyze account's crypto focus
            focus_analysis = self.twitter_service.analyze_account_crypto_focus(
                account['username'], days=14
            )
            
            # Calculate recommendation score
            recommendation_score = (
                account['avg_engagement'] * 0.3 +
                focus_analysis['crypto_focus'] * 100 * 0.4 +
                (focus_analysis['engagement_ratio'] if focus_analysis['engagement_ratio'] != float('inf') else 10) * 0.3
            )
            
            recommendations.append({
                'username': account['username'],
                'name': account.get('name', ''),
                'verified': account.get('verified', False),
                'crypto_focus': focus_analysis['crypto_focus'],
                'avg_engagement': account['avg_engagement'],
                'recommendation_score': recommendation_score,
                'analysis': focus_analysis['analysis'],
                'reason': self._generate_recommendation_reason(account, focus_analysis)
            })
        
        # Sort by recommendation score
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return recommendations[:20]
    
    def _generate_recommendation_reason(self, account: Dict, focus_analysis: Dict) -> str:
        """Generate explanation for why this account is recommended"""
        reasons = []
        
        if focus_analysis['crypto_focus'] > 0.7:
            reasons.append("highly crypto-focused")
        elif focus_analysis['crypto_focus'] > 0.4:
            reasons.append("frequently discusses crypto")
        
        if account['avg_engagement'] > 100:
            reasons.append("high engagement")
        elif account['avg_engagement'] > 50:
            reasons.append("good engagement")
        
        if account.get('verified'):
            reasons.append("verified account")
        
        if focus_analysis.get('engagement_ratio', 1) > 1.5:
            reasons.append("crypto content performs well")
        
        return "Recommended for: " + ", ".join(reasons) if reasons else "Active crypto participant"