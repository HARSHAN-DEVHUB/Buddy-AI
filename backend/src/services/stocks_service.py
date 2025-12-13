"""
Stock Market Data Service
Fetches Indian and international stock data using yfinance and NSEpy
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Try to import nsepy for Indian stocks
try:
    from nsepy import get_history
    from nsepy.live import get_quote
    NSEPY_AVAILABLE = True
except ImportError:
    NSEPY_AVAILABLE = False
    logger.warning("NSEpy not available. Indian stock live data will be limited.")


class StocksService:
    """Service for fetching stock market data"""
    
    # Popular Indian stocks (NSE)
    INDIAN_STOCKS = [
        'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 
        'HINDUNILVR.NS', 'ICICIBANK.NS', 'SBIN.NS', 'BHARTIARTL.NS',
        'ITC.NS', 'KOTAKBANK.NS', 'LT.NS', 'AXISBANK.NS'
    ]
    
    # Popular US stocks
    US_STOCKS = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
        'META', 'NVDA', 'JPM', 'V', 'WMT'
    ]
    
    # Indian indices
    INDIAN_INDICES = [
        '^NSEI',  # NIFTY 50
        '^BSESN'  # SENSEX
    ]
    
    def __init__(self):
        """Initialize stocks service"""
        self.cache: Dict[str, Any] = {}
        self.cache_ttl = 300  # 5 minutes cache for stocks (less frequent updates)
    
    def get_current_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price for a stock symbol
        
        Args:
            symbol: Stock ticker (e.g., 'RELIANCE.NS', 'AAPL')
            
        Returns:
            Dictionary with price data
        """
        try:
            ticker = yf.Ticker(symbol)
            
            # Get current data
            info = ticker.info
            history = ticker.history(period='5d')
            
            if history.empty:
                raise ValueError(f"No data available for {symbol}")
            
            latest = history.iloc[-1]
            previous = history.iloc[-2] if len(history) > 1 else latest
            
            current_price = latest['Close']
            open_price = latest['Open']
            high = latest['High']
            low = latest['Low']
            volume = latest['Volume']
            
            # Calculate 24h change
            change_24h = current_price - previous['Close']
            change_percent_24h = (change_24h / previous['Close']) * 100 if previous['Close'] > 0 else 0
            
            return {
                'symbol': symbol,
                'price': float(current_price),
                'open_price': float(open_price),
                'high': float(high),
                'low': float(low),
                'close': float(current_price),
                'volume': float(volume),
                'change_24h': float(change_24h),
                'change_percent_24h': float(change_percent_24h),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE'),
                'eps': info.get('trailingEps'),
                'timestamp': int(datetime.now().timestamp() * 1000)
            }
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            raise
    
    def get_all_prices(self, market: str = 'indian') -> List[Dict[str, Any]]:
        """
        Get current prices for popular stocks
        
        Args:
            market: 'indian' or 'us'
            
        Returns:
            List of price dictionaries
        """
        symbols = self.INDIAN_STOCKS if market == 'indian' else self.US_STOCKS
        results = []
        
        for symbol in symbols:
            try:
                price_data = self.get_current_price(symbol)
                results.append(price_data)
            except Exception as e:
                logger.warning(f"Failed to fetch {symbol}: {e}")
                continue
        
        return results
    
    def get_historical_data(
        self,
        symbol: str,
        interval: str = '1d',
        period: str = '1mo',
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get historical stock data (OHLCV)
        
        Args:
            symbol: Stock ticker
            interval: Timeframe (1m, 5m, 15m, 1h, 1d, 1wk, 1mo)
            period: Period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
            start_date: Start datetime (optional)
            end_date: End datetime (optional)
            
        Returns:
            List of OHLCV dictionaries
        """
        try:
            ticker = yf.Ticker(symbol)
            
            if start_date and end_date:
                df = ticker.history(
                    start=start_date,
                    end=end_date,
                    interval=interval
                )
            else:
                df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                return []
            
            ohlcv_data = []
            for idx, row in df.iterrows():
                ohlcv_data.append({
                    'timestamp': idx.to_pydatetime(),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': float(row['Volume']),
                })
            
            return ohlcv_data
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            raise
    
    def get_index_data(self, index: str = '^NSEI') -> Dict[str, Any]:
        """
        Get Indian index data (NIFTY 50, SENSEX)
        
        Args:
            index: Index symbol (^NSEI for NIFTY 50, ^BSESN for SENSEX)
            
        Returns:
            Index data dictionary
        """
        try:
            return self.get_current_price(index)
        except Exception as e:
            logger.error(f"Error fetching index data for {index}: {e}")
            raise
    
    def get_market_overview(self, market: str = 'indian') -> Dict[str, Any]:
        """
        Get market overview with top gainers, losers, and volume leaders
        
        Args:
            market: 'indian' or 'us'
            
        Returns:
            Market overview statistics
        """
        try:
            all_prices = self.get_all_prices(market)
            
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
                'mostActive': sorted_by_volume[:5],
                'market': market
            }
        except Exception as e:
            logger.error(f"Error getting market overview: {e}")
            raise
    
    def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get detailed company information
        
        Args:
            symbol: Stock ticker
            
        Returns:
            Company information dictionary
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', info.get('shortName', 'N/A')),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'marketCap': info.get('marketCap'),
                'peRatio': info.get('trailingPE'),
                'dividendYield': info.get('dividendYield'),
                'eps': info.get('trailingEps'),
                'beta': info.get('beta'),
                'yearHigh': info.get('fiftyTwoWeekHigh'),
                'yearLow': info.get('fiftyTwoWeekLow'),
                'avgVolume': info.get('averageVolume'),
                'description': info.get('longBusinessSummary', '')
            }
        except Exception as e:
            logger.error(f"Error fetching company info for {symbol}: {e}")
            raise
    
    def search_stocks(self, query: str, limit: int = 10) -> List[Dict[str, str]]:
        """
        Search for stocks by name or symbol
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of matching stocks
        """
        # This is a simple implementation
        # In production, use a proper search API or database
        all_symbols = self.INDIAN_STOCKS + self.US_STOCKS
        matches = [s for s in all_symbols if query.upper() in s.upper()]
        
        results = []
        for symbol in matches[:limit]:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                results.append({
                    'symbol': symbol,
                    'name': info.get('longName', info.get('shortName', symbol))
                })
            except:
                continue
        
        return results


# Singleton instance
stocks_service = StocksService()
