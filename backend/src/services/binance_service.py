"""
Binance API Service for Cryptocurrency Data
Fetches real-time and historical crypto market data
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class BinanceService:
    """Service for interacting with Binance API"""
    
    # Popular crypto symbols
    POPULAR_SYMBOLS = [
        'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 
        'ADAUSDT', 'DOGEUSDT', 'SOLUSDT', 'DOTUSDT',
        'MATICUSDT', 'LTCUSDT', 'AVAXUSDT', 'LINKUSDT'
    ]
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize Binance client
        For public data, api_key and api_secret are not required
        """
        self.client = Client(api_key, api_secret)
        self.cache: Dict[str, Any] = {}
        self.cache_ttl = 60  # Cache for 60 seconds
        
    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price for a symbol
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            
        Returns:
            Dictionary with price data
        """
        try:
            ticker = self.client.get_ticker(symbol=symbol)
            
            return {
                'symbol': symbol,
                'price': float(ticker['lastPrice']),
                'open_price': float(ticker['openPrice']),
                'high': float(ticker['highPrice']),
                'low': float(ticker['lowPrice']),
                'close': float(ticker['lastPrice']),
                'volume': float(ticker['volume']),
                'change_24h': float(ticker['priceChange']),
                'change_percent_24h': float(ticker['priceChangePercent']),
                'bid': float(ticker.get('bidPrice', 0)),
                'ask': float(ticker.get('askPrice', 0)),
                'timestamp': int(ticker['closeTime'])
            }
        except BinanceAPIException as e:
            logger.error(f"Binance API error for {symbol}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            raise
    
    def get_all_prices(self) -> List[Dict[str, Any]]:
        """
        Get current prices for all popular symbols
        
        Returns:
            List of price dictionaries
        """
        try:
            all_tickers = self.client.get_ticker()
            
            # Filter for popular symbols
            popular_tickers = [
                t for t in all_tickers 
                if t['symbol'] in self.POPULAR_SYMBOLS
            ]
            
            results = []
            for ticker in popular_tickers:
                results.append({
                    'symbol': ticker['symbol'],
                    'price': float(ticker['lastPrice']),
                    'open_price': float(ticker['openPrice']),
                    'high': float(ticker['highPrice']),
                    'low': float(ticker['lowPrice']),
                    'close': float(ticker['lastPrice']),
                    'volume': float(ticker['volume']),
                    'change_24h': float(ticker['priceChange']),
                    'change_percent_24h': float(ticker['priceChangePercent']),
                    'timestamp': int(ticker['closeTime'])
                })
            
            return results
        except Exception as e:
            logger.error(f"Error fetching all prices: {e}")
            raise
    
    def get_historical_klines(
        self,
        symbol: str,
        interval: str = '1h',
        limit: int = 500,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get historical candlestick data (OHLCV)
        
        Args:
            symbol: Trading pair
            interval: Timeframe (1m, 5m, 15m, 1h, 4h, 1d, 1w)
            limit: Number of candles (max 1000)
            start_time: Start datetime
            end_time: End datetime
            
        Returns:
            List of OHLCV dictionaries
        """
        try:
            # Convert interval to Binance format
            interval_map = {
                '1m': Client.KLINE_INTERVAL_1MINUTE,
                '5m': Client.KLINE_INTERVAL_5MINUTE,
                '15m': Client.KLINE_INTERVAL_15MINUTE,
                '30m': Client.KLINE_INTERVAL_30MINUTE,
                '1h': Client.KLINE_INTERVAL_1HOUR,
                '4h': Client.KLINE_INTERVAL_4HOUR,
                '1d': Client.KLINE_INTERVAL_1DAY,
                '1w': Client.KLINE_INTERVAL_1WEEK,
            }
            
            binance_interval = interval_map.get(interval, Client.KLINE_INTERVAL_1HOUR)
            
            # Prepare parameters
            params = {
                'symbol': symbol,
                'interval': binance_interval,
                'limit': min(limit, 1000)
            }
            
            if start_time:
                params['startTime'] = int(start_time.timestamp() * 1000)
            if end_time:
                params['endTime'] = int(end_time.timestamp() * 1000)
            
            klines = self.client.get_klines(**params)
            
            # Parse klines data
            ohlcv_data = []
            for kline in klines:
                ohlcv_data.append({
                    'timestamp': datetime.fromtimestamp(kline[0] / 1000),
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5]),
                    'close_time': datetime.fromtimestamp(kline[6] / 1000),
                    'quote_volume': float(kline[7]),
                    'trades': int(kline[8])
                })
            
            return ohlcv_data
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            raise
    
    def get_orderbook(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get order book data
        
        Args:
            symbol: Trading pair
            limit: Number of levels (default 20)
            
        Returns:
            Order book with bids and asks
        """
        try:
            depth = self.client.get_order_book(symbol=symbol, limit=limit)
            
            return {
                'symbol': symbol,
                'bids': [[float(price), float(qty)] for price, qty in depth['bids']],
                'asks': [[float(price), float(qty)] for price, qty in depth['asks']],
                'timestamp': datetime.now()
            }
        except Exception as e:
            logger.error(f"Error fetching orderbook for {symbol}: {e}")
            raise
    
    def get_market_overview(self) -> Dict[str, Any]:
        """
        Get market overview with top gainers, losers, and volume leaders
        
        Returns:
            Market overview statistics
        """
        try:
            all_prices = self.get_all_prices()
            
            if not all_prices:
                return {
                    'totalVolume': 0,
                    'avgChange': 0,
                    'topGainers': [],
                    'topLosers': [],
                    'mostActive': []
                }
            
            # Calculate statistics
            total_volume = sum(p['volume'] for p in all_prices)
            avg_change = sum(p['change_percent_24h'] for p in all_prices) / len(all_prices)
            
            # Sort for top gainers and losers
            sorted_by_change = sorted(all_prices, key=lambda x: x['change_percent_24h'], reverse=True)
            sorted_by_volume = sorted(all_prices, key=lambda x: x['volume'], reverse=True)
            
            return {
                'totalVolume': total_volume,
                'avgChange': avg_change,
                'topGainers': sorted_by_change[:5],
                'topLosers': sorted_by_change[-5:],
                'mostActive': sorted_by_volume[:5]
            }
        except Exception as e:
            logger.error(f"Error getting market overview: {e}")
            raise
    
    def get_symbol_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get detailed symbol information
        
        Args:
            symbol: Trading pair
            
        Returns:
            Symbol information
        """
        try:
            info = self.client.get_symbol_info(symbol)
            
            return {
                'symbol': info['symbol'],
                'status': info['status'],
                'baseAsset': info['baseAsset'],
                'quoteAsset': info['quoteAsset'],
                'pricePrecision': info['quotePrecision'],
                'quantityPrecision': info['baseAssetPrecision'],
            }
        except Exception as e:
            logger.error(f"Error fetching symbol info for {symbol}: {e}")
            raise


# Singleton instance
binance_service = BinanceService()
