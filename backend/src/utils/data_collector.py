"""
Data Collection Utilities
Tools for collecting and storing market data
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import logging

from src.services.binance_service import binance_service
from src.services.stocks_service import stocks_service
from src.models.market import MarketData, OHLCV, MarketType

logger = logging.getLogger(__name__)


class DataCollector:
    """Utility class for collecting and storing market data"""
    
    def __init__(self, db: Session):
        """
        Initialize data collector
        
        Args:
            db: Database session
        """
        self.db = db
    
    def collect_crypto_prices(self, symbols: Optional[List[str]] = None) -> int:
        """
        Collect current crypto prices and store in database
        
        Args:
            symbols: List of symbols (defaults to popular ones)
            
        Returns:
            Number of prices collected
        """
        try:
            if symbols is None:
                # Get all popular symbols
                all_prices = binance_service.get_all_prices()
            else:
                all_prices = []
                for symbol in symbols:
                    try:
                        price_data = binance_service.get_current_price(symbol)
                        all_prices.append(price_data)
                    except Exception as e:
                        logger.warning(f"Failed to fetch {symbol}: {e}")
                        continue
            
            # Store in database
            count = 0
            for price_data in all_prices:
                try:
                    db_market_data = MarketData(
                        symbol=price_data['symbol'],
                        market=MarketType.CRYPTO,
                        price=price_data['price'],
                        open_price=price_data.get('open_price'),
                        high=price_data.get('high'),
                        low=price_data.get('low'),
                        close=price_data.get('close'),
                        volume=price_data.get('volume'),
                        change_24h=price_data.get('change_24h'),
                        change_percent_24h=price_data.get('change_percent_24h')
                    )
                    self.db.add(db_market_data)
                    count += 1
                except Exception as e:
                    logger.warning(f"Failed to store {price_data['symbol']}: {e}")
                    continue
            
            self.db.commit()
            logger.info(f"Collected {count} crypto prices")
            return count
            
        except Exception as e:
            logger.error(f"Error collecting crypto prices: {e}")
            self.db.rollback()
            raise
    
    def collect_stock_prices(self, symbols: Optional[List[str]] = None, market: str = 'indian') -> int:
        """
        Collect current stock prices and store in database
        
        Args:
            symbols: List of symbols (defaults to popular ones)
            market: 'indian' or 'us'
            
        Returns:
            Number of prices collected
        """
        try:
            if symbols is None:
                all_prices = stocks_service.get_all_prices(market)
            else:
                all_prices = []
                for symbol in symbols:
                    try:
                        price_data = stocks_service.get_current_price(symbol)
                        all_prices.append(price_data)
                    except Exception as e:
                        logger.warning(f"Failed to fetch {symbol}: {e}")
                        continue
            
            # Store in database
            count = 0
            for price_data in all_prices:
                try:
                    db_market_data = MarketData(
                        symbol=price_data['symbol'],
                        market=MarketType.STOCK,
                        price=price_data['price'],
                        open_price=price_data.get('open_price'),
                        high=price_data.get('high'),
                        low=price_data.get('low'),
                        close=price_data.get('close'),
                        volume=price_data.get('volume'),
                        change_24h=price_data.get('change_24h'),
                        change_percent_24h=price_data.get('change_percent_24h')
                    )
                    self.db.add(db_market_data)
                    count += 1
                except Exception as e:
                    logger.warning(f"Failed to store {price_data['symbol']}: {e}")
                    continue
            
            self.db.commit()
            logger.info(f"Collected {count} stock prices")
            return count
            
        except Exception as e:
            logger.error(f"Error collecting stock prices: {e}")
            self.db.rollback()
            raise
    
    def collect_historical_ohlcv(
        self,
        symbol: str,
        market_type: MarketType,
        timeframe: str = '1h',
        limit: int = 500
    ) -> int:
        """
        Collect historical OHLCV data and store in database
        
        Args:
            symbol: Trading symbol
            market_type: Market type enum
            timeframe: Candle timeframe
            limit: Number of candles
            
        Returns:
            Number of candles stored
        """
        try:
            # Fetch historical data
            if market_type == MarketType.CRYPTO:
                ohlcv_data = binance_service.get_historical_klines(
                    symbol=symbol,
                    interval=timeframe,
                    limit=limit
                )
            elif market_type == MarketType.STOCK:
                interval_map = {
                    '1h': '1h', '4h': '4h', '1d': '1d', '1w': '1wk'
                }
                yf_interval = interval_map.get(timeframe, '1d')
                
                ohlcv_data = stocks_service.get_historical_data(
                    symbol=symbol,
                    interval=yf_interval,
                    period='1y'
                )
            else:
                raise ValueError(f"Unsupported market type: {market_type}")
            
            # Store in database
            count = 0
            for candle in ohlcv_data:
                try:
                    db_ohlcv = OHLCV(
                        symbol=symbol,
                        market=market_type,
                        timeframe=timeframe,
                        timestamp=candle['timestamp'],
                        open=candle['open'],
                        high=candle['high'],
                        low=candle['low'],
                        close=candle['close'],
                        volume=candle['volume']
                    )
                    self.db.merge(db_ohlcv)  # Use merge to avoid duplicates
                    count += 1
                except Exception as e:
                    logger.warning(f"Failed to store candle: {e}")
                    continue
            
            self.db.commit()
            logger.info(f"Collected {count} OHLCV candles for {symbol}")
            return count
            
        except Exception as e:
            logger.error(f"Error collecting OHLCV data for {symbol}: {e}")
            self.db.rollback()
            raise
    
    def bulk_collect_historical_data(
        self,
        symbols: List[str],
        market_type: MarketType,
        timeframe: str = '1h',
        limit: int = 500
    ) -> dict:
        """
        Collect historical data for multiple symbols
        
        Args:
            symbols: List of symbols
            market_type: Market type
            timeframe: Candle timeframe
            limit: Number of candles per symbol
            
        Returns:
            Dictionary with collection statistics
        """
        results = {
            'total_symbols': len(symbols),
            'successful': 0,
            'failed': 0,
            'total_candles': 0
        }
        
        for symbol in symbols:
            try:
                count = self.collect_historical_ohlcv(
                    symbol=symbol,
                    market_type=market_type,
                    timeframe=timeframe,
                    limit=limit
                )
                results['successful'] += 1
                results['total_candles'] += count
            except Exception as e:
                logger.warning(f"Failed to collect data for {symbol}: {e}")
                results['failed'] += 1
                continue
        
        logger.info(f"Bulk collection complete: {results}")
        return results


def create_data_collector(db: Session) -> DataCollector:
    """Factory function to create DataCollector instance"""
    return DataCollector(db)
