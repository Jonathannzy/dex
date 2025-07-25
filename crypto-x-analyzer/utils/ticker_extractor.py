import re
import requests
import json
from typing import List, Dict, Set
import pandas as pd

class TickerExtractor:
    def __init__(self):
        self.crypto_symbols = self._load_crypto_symbols()
        self.cashtag_pattern = re.compile(r'\$([A-Z]{2,10})')
        self.ticker_patterns = [
            re.compile(r'\b([A-Z]{2,6})/USD\b'),
            re.compile(r'\b([A-Z]{2,6})/USDT\b'),
            re.compile(r'\b([A-Z]{2,6})-USD\b'),
            re.compile(r'\b([A-Z]{2,6})USD\b'),
            re.compile(r'\b([A-Z]{2,6})\s+(?:coin|token|crypto)\b', re.IGNORECASE),
        ]
        
    def _load_crypto_symbols(self) -> Set[str]:
        """Load known cryptocurrency symbols from CoinMarketCap API or fallback list"""
        try:
            # Fallback list of top cryptocurrencies
            top_cryptos = {
                'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'TRX', 'MATIC', 'DOT',
                'AVAX', 'SHIB', 'LTC', 'ATOM', 'UNI', 'LINK', 'XMR', 'BCH', 'ETC', 'FIL',
                'ICP', 'APT', 'NEAR', 'VET', 'ALGO', 'FLOW', 'MANA', 'SAND', 'AXS', 'CHZ',
                'ENJ', 'BAT', 'ZEC', 'DASH', 'COMP', 'YFI', 'SNX', 'MKR', 'AAVE', 'CRV',
                'SUSHI', '1INCH', 'ALPHA', 'RUNE', 'CAKE', 'LUNA', 'UST', 'TERRA', 'OSMO',
                'JUNO', 'SCRT', 'KAVA', 'BAND', 'REN', 'LRC', 'OMG', 'ZRX', 'BAL', 'REP',
                'KNC', 'GRT', 'FTM', 'ONE', 'HARMONY', 'IOTX', 'ZIL', 'ONT', 'ICX', 'QTUM',
                'WAVES', 'LSK', 'ARK', 'NANO', 'XTZ', 'KSM', 'EGLD', 'THETA', 'TFUEL',
                'HBAR', 'IOTA', 'MIOTA', 'NEO', 'GAS', 'XEM', 'XLM', 'XDC', 'DENT', 'HOT',
                'WIN', 'BTT', 'STMX', 'ANKR', 'CELR', 'CKB', 'RSR', 'OGN', 'NKN', 'CTSI',
                'AUDIO', 'BADGER', 'REN', 'LPT', 'NMR', 'MLN', 'BNT', 'OCEAN', 'STORJ',
                'SKL', 'API3', 'MASK', 'AMP', 'FORTH', 'TRB', 'REQ', 'ACH', 'CLV', 'FARM',
                'FIDA', 'RAY', 'SRM', 'STEP', 'ROPE', 'COPE', 'MEDIA', 'TULIP', 'SLIM',
                'SAMO', 'NINJA', 'GRAPE', 'ORCA', 'MNGO', 'MAPS', 'ATLAS', 'POLIS', 'STAR',
                'GENE', 'DFL', 'CHEEMS', 'BONK', 'MYRO', 'WIF', 'POPCAT', 'MEW', 'MOTHER',
                'DADDY', 'PEPE', 'FLOKI', 'BABYDOGE', 'SAFEMOON', 'KISHU', 'ELON', 'DOGELON'
            }
            return top_cryptos
        except Exception:
            # Return minimal set if API fails
            return {'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'MATIC', 'DOT', 'AVAX'}
    
    def extract_tickers_from_text(self, text: str) -> List[Dict]:
        """Extract cryptocurrency tickers from text"""
        tickers = []
        text_upper = text.upper()
        
        # Extract cashtags ($BTC, $ETH, etc.)
        cashtags = self.cashtag_pattern.findall(text_upper)
        for tag in cashtags:
            if tag in self.crypto_symbols:
                tickers.append({
                    'symbol': tag,
                    'confidence': 0.9,
                    'method': 'cashtag',
                    'context': self._get_context(text, f'${tag}')
                })
        
        # Extract using various patterns
        for pattern in self.ticker_patterns:
            matches = pattern.findall(text_upper)
            for match in matches:
                if match in self.crypto_symbols:
                    tickers.append({
                        'symbol': match,
                        'confidence': 0.7,
                        'method': 'pattern',
                        'context': self._get_context(text, match)
                    })
        
        # Remove duplicates and sort by confidence
        unique_tickers = {}
        for ticker in tickers:
            symbol = ticker['symbol']
            if symbol not in unique_tickers or ticker['confidence'] > unique_tickers[symbol]['confidence']:
                unique_tickers[symbol] = ticker
        
        return list(unique_tickers.values())
    
    def _get_context(self, text: str, ticker: str, window: int = 20) -> str:
        """Get surrounding context for a ticker mention"""
        try:
            index = text.upper().find(ticker.upper())
            if index == -1:
                return text[:50]
            
            start = max(0, index - window)
            end = min(len(text), index + len(ticker) + window)
            return text[start:end].strip()
        except:
            return text[:50]
    
    def analyze_sentiment_context(self, context: str) -> Dict:
        """Analyze sentiment and trading signals in the context"""
        bullish_keywords = ['moon', 'pump', 'bull', 'buy', 'long', 'bullish', 'gem', 'alpha', 'rocket', '🚀', '🌙', 'diamond hands', 'hodl']
        bearish_keywords = ['dump', 'bear', 'sell', 'short', 'bearish', 'crash', 'paper hands', 'rug', 'scam']
        neutral_keywords = ['dip', 'consolidation', 'sideways', 'range', 'support', 'resistance']
        
        context_lower = context.lower()
        
        bullish_count = sum(1 for word in bullish_keywords if word in context_lower)
        bearish_count = sum(1 for word in bearish_keywords if word in context_lower)
        neutral_count = sum(1 for word in neutral_keywords if word in context_lower)
        
        total_signals = bullish_count + bearish_count + neutral_count
        
        if total_signals == 0:
            return {'sentiment': 'neutral', 'confidence': 0.0, 'signals': {}}
        
        sentiment_score = (bullish_count - bearish_count) / total_signals
        
        if sentiment_score > 0.3:
            sentiment = 'bullish'
        elif sentiment_score < -0.3:
            sentiment = 'bearish'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'confidence': abs(sentiment_score),
            'signals': {
                'bullish': bullish_count,
                'bearish': bearish_count,
                'neutral': neutral_count
            }
        }
    
    def extract_price_targets(self, text: str) -> List[Dict]:
        """Extract price predictions and targets from text"""
        price_patterns = [
            re.compile(r'\$(\d+(?:,\d{3})*(?:\.\d+)?)', re.IGNORECASE),
            re.compile(r'(\d+(?:,\d{3})*(?:\.\d+)?)k', re.IGNORECASE),
            re.compile(r'target.*?(\d+(?:\.\d+)?)', re.IGNORECASE),
            re.compile(r'resistance.*?(\d+(?:\.\d+)?)', re.IGNORECASE),
            re.compile(r'support.*?(\d+(?:\.\d+)?)', re.IGNORECASE),
        ]
        
        targets = []
        for pattern in price_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                try:
                    price_str = match.group(1)
                    if 'k' in match.group(0).lower():
                        price = float(price_str) * 1000
                    else:
                        price = float(price_str.replace(',', ''))
                    
                    targets.append({
                        'price': price,
                        'context': self._get_context(text, match.group(0)),
                        'type': self._classify_price_mention(match.group(0))
                    })
                except ValueError:
                    continue
        
        return targets
    
    def _classify_price_mention(self, price_text: str) -> str:
        """Classify the type of price mention"""
        text_lower = price_text.lower()
        if 'target' in text_lower:
            return 'target'
        elif 'resistance' in text_lower:
            return 'resistance'
        elif 'support' in text_lower:
            return 'support'
        elif '$' in text_lower:
            return 'prediction'
        else:
            return 'mention'