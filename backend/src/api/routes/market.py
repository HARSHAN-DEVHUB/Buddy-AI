"""
Market Data API Routes
Endpoints for fetching real-time and historical market data
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta
import logging

from src.config.database import get_db
from src.services.binance_service import binance_service
from src.services.stocks_service import stocks_service
from src.services.indicators_service import indicators_service
from src.models.market import MarketData, OHLCV, MarketType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/market", tags=["market"])


@router.get("/price/{market}/{symbol}")
async def get_current_price(
    market: str,
    symbol: str,
    db: Session = Depends(get_db)
):
    """
    Get current price for a symbol
    
    Args:
        market: Market type (forex, crypto, stock)
        symbol: Trading symbol (e.g., BTCUSDT, AAPL, RELIANCE.NS)
    """
    try:
        market_lower = market.lower()
        
        if market_lower == 'crypto':
            price_data = binance_service.get_current_price(symbol)
        elif market_lower in ['stock', 'stocks']:
            price_data = stocks_service.get_current_price(symbol)
        elif market_lower == 'forex':
            # Forex not implemented yet
            raise HTTPException(status_code=501, detail="Forex data not yet implemented")
        else:
            raise HTTPException(status_code=400, detail=f"Invalid market type: {market}")
        
        # Optionally save to database
        try:
            market_type = MarketType.CRYPTO if market_lower == 'crypto' else MarketType.STOCK
            db_market_data = MarketData(
                symbol=symbol,
                market=market_type,
                price=price_data['price'],
                open_price=price_data.get('open_price'),
                high=price_data.get('high'),
                low=price_data.get('low'),
                close=price_data.get('close'),
                volume=price_data.get('volume'),
                change_24h=price_data.get('change_24h'),
                change_percent_24h=price_data.get('change_percent_24h')
            )
            db.add(db_market_data)
            db.commit()
        except Exception as e:
            logger.warning(f"Failed to save market data to DB: {e}")
            db.rollback()
        
        return {
            "success": True,
            "data": price_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{market}/{symbol}")
async def get_historical_data(
    market: str,
    symbol: str,
    timeframe: str = Query("1h", description="Timeframe (1m, 5m, 15m, 1h, 4h, 1d)"),
    limit: int = Query(100, ge=1, le=1000, description="Number of candles"),
    db: Session = Depends(get_db)
):
    """
    Get historical OHLCV data
    
    Args:
        market: Market type
        symbol: Trading symbol
        timeframe: Candle timeframe
        limit: Number of candles to fetch
    """
    try:
        market_lower = market.lower()
        
        if market_lower == 'crypto':
            ohlcv_data = binance_service.get_historical_klines(
                symbol=symbol,
                interval=timeframe,
                limit=limit
            )
        elif market_lower in ['stock', 'stocks']:
            # Map timeframe to yfinance format
            interval_map = {
                '1m': '1m', '5m': '5m', '15m': '15m', '30m': '30m',
                '1h': '1h', '4h': '4h', '1d': '1d', '1w': '1wk'
            }
            yf_interval = interval_map.get(timeframe, '1d')
            
            ohlcv_data = stocks_service.get_historical_data(
                symbol=symbol,
                interval=yf_interval,
                period='1mo' if limit <= 30 else '3mo'
            )
            ohlcv_data = ohlcv_data[:limit]  # Limit results
        else:
            raise HTTPException(status_code=400, detail=f"Invalid market type: {market}")
        
        # Optionally save to database
        try:
            market_type = MarketType.CRYPTO if market_lower == 'crypto' else MarketType.STOCK
            
            for candle in ohlcv_data[-10:]:  # Save last 10 candles to avoid overwhelming DB
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
                db.merge(db_ohlcv)  # Use merge to avoid duplicates
            
            db.commit()
        except Exception as e:
            logger.warning(f"Failed to save OHLCV data to DB: {e}")
            db.rollback()
        
        return {
            "success": True,
            "data": ohlcv_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching historical data for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/indicators/{market}/{symbol}")
async def get_technical_indicators(
    market: str,
    symbol: str,
    timeframe: str = Query("1h", description="Timeframe for indicators"),
    db: Session = Depends(get_db)
):
    """
    Get technical indicators for a symbol
    
    Args:
        market: Market type
        symbol: Trading symbol
        timeframe: Timeframe for calculation
    """
    try:
        # First, get historical data
        market_lower = market.lower()
        
        if market_lower == 'crypto':
            ohlcv_data = binance_service.get_historical_klines(
                symbol=symbol,
                interval=timeframe,
                limit=500  # Need enough data for indicators
            )
        elif market_lower in ['stock', 'stocks']:
            interval_map = {
                '1h': '1h', '4h': '4h', '1d': '1d', '1w': '1wk'
            }
            yf_interval = interval_map.get(timeframe, '1d')
            
            ohlcv_data = stocks_service.get_historical_data(
                symbol=symbol,
                interval=yf_interval,
                period='1y'  # Get more data for accurate indicators
            )
        else:
            raise HTTPException(status_code=400, detail=f"Invalid market type: {market}")
        
        if not ohlcv_data or len(ohlcv_data) < 50:
            raise HTTPException(
                status_code=400,
                detail="Insufficient data for indicator calculation"
            )
        
        # Calculate indicators
        indicators = indicators_service.calculate_all_indicators(ohlcv_data, symbol)
        
        # Add trend signal
        indicators['trendSignal'] = indicators_service.get_trend_signal(indicators)
        
        return {
            "success": True,
            "data": indicators
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating indicators for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/overview/{market}")
async def get_market_overview(
    market: str,
    db: Session = Depends(get_db)
):
    """
    Get market overview with top movers and statistics
    
    Args:
        market: Market type (crypto, stock)
    """
    try:
        market_lower = market.lower()
        
        if market_lower == 'crypto':
            overview = binance_service.get_market_overview()
        elif market_lower in ['stock', 'stocks']:
            # Default to Indian market
            overview = stocks_service.get_market_overview(market='indian')
        elif market_lower == 'forex':
            raise HTTPException(status_code=501, detail="Forex overview not yet implemented")
        else:
            raise HTTPException(status_code=400, detail=f"Invalid market type: {market}")
        
        return {
            "success": True,
            "data": overview
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching market overview for {market}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_symbols(
    query: str = Query(..., min_length=1, description="Search query"),
    market: Optional[str] = Query(None, description="Filter by market type"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Search for trading symbols
    
    Args:
        query: Search term
        market: Optional market filter
        limit: Max results
    """
    try:
        results = []
        
        # Search crypto if no market specified or crypto requested
        if not market or market.lower() == 'crypto':
            # Simple crypto search
            crypto_symbols = binance_service.POPULAR_SYMBOLS
            matches = [s for s in crypto_symbols if query.upper() in s]
            results.extend([{'symbol': s, 'market': 'crypto', 'name': s} for s in matches[:limit]])
        
        # Search stocks if no market specified or stock requested
        if not market or market.lower() in ['stock', 'stocks']:
            stock_results = stocks_service.search_stocks(query, limit)
            for stock in stock_results:
                results.append({
                    'symbol': stock['symbol'],
                    'market': 'stock',
                    'name': stock['name']
                })
        
        return {
            "success": True,
            "data": results[:limit]
        }
        
    except Exception as e:
        logger.error(f"Error searching symbols: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orderbook/{market}/{symbol}")
async def get_orderbook(
    market: str,
    symbol: str,
    limit: int = Query(20, ge=5, le=100)
):
    """
    Get order book data (only available for crypto)
    
    Args:
        market: Market type (must be crypto)
        symbol: Trading symbol
        limit: Depth levels
    """
    try:
        if market.lower() != 'crypto':
            raise HTTPException(
                status_code=400,
                detail="Order book only available for crypto market"
            )
        
        orderbook = binance_service.get_orderbook(symbol, limit)
        
        return {
            "success": True,
            "data": orderbook
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching orderbook for {symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
