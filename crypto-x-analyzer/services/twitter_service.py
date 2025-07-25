import tweepy
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import logging
from config import Config

class TwitterService:
    def __init__(self):
        self.client = self._initialize_client()
        self.logger = logging.getLogger(__name__)
        
    def _initialize_client(self):
        """Initialize Twitter API client"""
        try:
            if Config.TWITTER_BEARER_TOKEN:
                return tweepy.Client(bearer_token=Config.TWITTER_BEARER_TOKEN)
            else:
                return tweepy.Client(
                    consumer_key=Config.TWITTER_API_KEY,
                    consumer_secret=Config.TWITTER_API_SECRET,
                    access_token=Config.TWITTER_ACCESS_TOKEN,
                    access_token_secret=Config.TWITTER_ACCESS_TOKEN_SECRET
                )
        except Exception as e:
            self.logger.error(f"Failed to initialize Twitter client: {e}")
            return None
    
    def get_user_timeline(self, username: str, days: int = 7, max_tweets: int = 200) -> List[Dict]:
        """Fetch recent tweets from a user's timeline"""
        if not self.client:
            return []
        
        try:
            user = self.client.get_user(username=username)
            if not user.data:
                return []
            
            user_id = user.data.id
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            tweets = tweepy.Paginator(
                self.client.get_users_tweets,
                id=user_id,
                start_time=start_time,
                end_time=end_time,
                tweet_fields=['created_at', 'public_metrics', 'context_annotations', 'entities'],
                max_results=100
            ).flatten(limit=max_tweets)
            
            return [self._process_tweet(tweet) for tweet in tweets]
            
        except Exception as e:
            self.logger.error(f"Error fetching timeline for {username}: {e}")
            return []
    
    def get_user_feed(self, username: str, days: int = 7, max_tweets: int = 500) -> List[Dict]:
        """Fetch the user's home timeline (their feed)"""
        if not self.client:
            return []
        
        try:
            # Note: This requires user authentication and may not work with bearer token only
            tweets = tweepy.Paginator(
                self.client.get_home_timeline,
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'context_annotations', 'entities'],
                user_fields=['username', 'name', 'verified'],
                expansions=['author_id'],
                max_results=100
            ).flatten(limit=max_tweets)
            
            processed_tweets = []
            for tweet in tweets:
                # Filter tweets by date
                if tweet.created_at and tweet.created_at >= datetime.utcnow() - timedelta(days=days):
                    processed_tweets.append(self._process_tweet(tweet))
            
            return processed_tweets
            
        except Exception as e:
            self.logger.error(f"Error fetching feed: {e}")
            # Fallback to searching for crypto-related tweets
            return self.search_crypto_tweets(days=days, max_tweets=max_tweets)
    
    def search_crypto_tweets(self, days: int = 7, max_tweets: int = 1000) -> List[Dict]:
        """Search for cryptocurrency-related tweets"""
        if not self.client:
            return []
        
        try:
            # Build search query for crypto-related content
            crypto_terms = ['bitcoin', 'ethereum', 'crypto', 'altcoin', 'defi', '$BTC', '$ETH']
            query = ' OR '.join(crypto_terms) + ' -is:retweet lang:en'
            
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=query,
                start_time=start_time,
                end_time=end_time,
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'context_annotations', 'entities'],
                user_fields=['username', 'name', 'verified'],
                expansions=['author_id'],
                max_results=100
            ).flatten(limit=max_tweets)
            
            return [self._process_tweet(tweet) for tweet in tweets]
            
        except Exception as e:
            self.logger.error(f"Error searching crypto tweets: {e}")
            return []
    
    def get_trending_crypto_accounts(self, limit: int = 50) -> List[Dict]:
        """Analyze accounts that frequently tweet about crypto"""
        crypto_tweets = self.search_crypto_tweets(days=3, max_tweets=2000)
        
        # Count tweets per author
        author_counts = {}
        author_engagement = {}
        
        for tweet in crypto_tweets:
            author_id = tweet.get('author_id')
            if not author_id:
                continue
            
            if author_id not in author_counts:
                author_counts[author_id] = {
                    'count': 0,
                    'total_likes': 0,
                    'total_retweets': 0,
                    'total_replies': 0,
                    'username': tweet.get('author_username', ''),
                    'name': tweet.get('author_name', ''),
                    'verified': tweet.get('author_verified', False)
                }
            
            author_counts[author_id]['count'] += 1
            author_counts[author_id]['total_likes'] += tweet.get('like_count', 0)
            author_counts[author_id]['total_retweets'] += tweet.get('retweet_count', 0)
            author_counts[author_id]['total_replies'] += tweet.get('reply_count', 0)
        
        # Calculate engagement scores
        trending_accounts = []
        for author_id, data in author_counts.items():
            if data['count'] >= 3:  # At least 3 crypto tweets
                engagement_score = (
                    data['total_likes'] * 1 +
                    data['total_retweets'] * 3 +
                    data['total_replies'] * 2
                ) / data['count']  # Average engagement per tweet
                
                trending_accounts.append({
                    'author_id': author_id,
                    'username': data['username'],
                    'name': data['name'],
                    'verified': data['verified'],
                    'tweet_count': data['count'],
                    'avg_engagement': engagement_score,
                    'total_engagement': data['total_likes'] + data['total_retweets'] + data['total_replies']
                })
        
        # Sort by engagement score
        trending_accounts.sort(key=lambda x: x['avg_engagement'], reverse=True)
        return trending_accounts[:limit]
    
    def analyze_account_crypto_focus(self, username: str, days: int = 30) -> Dict:
        """Analyze how crypto-focused an account is"""
        tweets = self.get_user_timeline(username, days=days, max_tweets=200)
        
        if not tweets:
            return {'crypto_focus': 0, 'analysis': 'No tweets found'}
        
        total_tweets = len(tweets)
        crypto_tweets = 0
        crypto_keywords = Config.CRYPTO_KEYWORDS
        
        for tweet in tweets:
            text = tweet.get('text', '').lower()
            if any(keyword in text for keyword in crypto_keywords):
                crypto_tweets += 1
        
        crypto_focus = crypto_tweets / total_tweets if total_tweets > 0 else 0
        
        # Calculate average engagement for crypto vs non-crypto tweets
        crypto_engagement = []
        non_crypto_engagement = []
        
        for tweet in tweets:
            text = tweet.get('text', '').lower()
            engagement = tweet.get('like_count', 0) + tweet.get('retweet_count', 0)
            
            if any(keyword in text for keyword in crypto_keywords):
                crypto_engagement.append(engagement)
            else:
                non_crypto_engagement.append(engagement)
        
        avg_crypto_engagement = sum(crypto_engagement) / len(crypto_engagement) if crypto_engagement else 0
        avg_non_crypto_engagement = sum(non_crypto_engagement) / len(non_crypto_engagement) if non_crypto_engagement else 0
        
        return {
            'username': username,
            'crypto_focus': crypto_focus,
            'total_tweets': total_tweets,
            'crypto_tweets': crypto_tweets,
            'avg_crypto_engagement': avg_crypto_engagement,
            'avg_non_crypto_engagement': avg_non_crypto_engagement,
            'engagement_ratio': avg_crypto_engagement / avg_non_crypto_engagement if avg_non_crypto_engagement > 0 else float('inf'),
            'analysis': self._generate_focus_analysis(crypto_focus, avg_crypto_engagement, avg_non_crypto_engagement)
        }
    
    def _process_tweet(self, tweet) -> Dict:
        """Process raw tweet data into standardized format"""
        metrics = getattr(tweet, 'public_metrics', {}) or {}
        
        return {
            'id': getattr(tweet, 'id', ''),
            'text': getattr(tweet, 'text', ''),
            'created_at': getattr(tweet, 'created_at', None),
            'author_id': getattr(tweet, 'author_id', ''),
            'like_count': metrics.get('like_count', 0),
            'retweet_count': metrics.get('retweet_count', 0),
            'reply_count': metrics.get('reply_count', 0),
            'quote_count': metrics.get('quote_count', 0),
            'entities': getattr(tweet, 'entities', {}),
            'context_annotations': getattr(tweet, 'context_annotations', [])
        }
    
    def _generate_focus_analysis(self, crypto_focus: float, crypto_eng: float, non_crypto_eng: float) -> str:
        """Generate human-readable analysis of account's crypto focus"""
        if crypto_focus >= 0.8:
            focus_level = "heavily crypto-focused"
        elif crypto_focus >= 0.5:
            focus_level = "crypto-focused"
        elif crypto_focus >= 0.2:
            focus_level = "occasionally discusses crypto"
        else:
            focus_level = "rarely discusses crypto"
        
        if crypto_eng > non_crypto_eng * 1.5:
            engagement_note = "Their crypto content performs significantly better."
        elif crypto_eng > non_crypto_eng:
            engagement_note = "Their crypto content performs better."
        elif crypto_eng < non_crypto_eng * 0.5:
            engagement_note = "Their non-crypto content performs much better."
        else:
            engagement_note = "Similar engagement across content types."
        
        return f"This account is {focus_level} ({crypto_focus:.1%} of tweets). {engagement_note}"
    
    def rate_limit_check(self):
        """Check Twitter API rate limits"""
        if not self.client:
            return None
        
        try:
            rate_limit = self.client.get_rate_limit_status()
            return rate_limit
        except Exception as e:
            self.logger.error(f"Error checking rate limits: {e}")
            return None