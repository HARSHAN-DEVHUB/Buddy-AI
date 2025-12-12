"""
Market data models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Index
from sqlalchemy.sql import func
from src.config.database import Base
import enum


class MarketType(enum.Enum):
    """Market types"""
    FOREX = "forex"
    CRYPTO = "crypto"
    STOCK = "stock"


class MarketData(Base):
    """Model for storing market price data"""
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    
    # Identifiers
    symbol = Column(String, index=True, nullable=False)
    market = Column(Enum(MarketType), nullable=False)
    
    # Price data
    price = Column(Float, nullable=False)
    open_price = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    close = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    
    # Changes
    change_24h = Column(Float, nullable=True)
    change_percent_24h = Column(Float, nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Create composite index for efficient queries
    __table_args__ = (
        Index('idx_symbol_market_timestamp', 'symbol', 'market', 'timestamp'),
    )

    def __repr__(self):
        return f"<MarketData {self.symbol} @ {self.price}>"


class OHLCV(Base):
    """Model for storing OHLCV candlestick data"""
    __tablename__ = "ohlcv_data"

    id = Column(Integer, primary_key=True, index=True)
    
    # Identifiers
    symbol = Column(String, index=True, nullable=False)
    market = Column(Enum(MarketType), nullable=False)
    timeframe = Column(String, nullable=False)  # 1m, 5m, 15m, 1h, 4h, 1d, etc.
    
    # OHLCV data
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    
    # Create composite index
    __table_args__ = (
        Index('idx_ohlcv_lookup', 'symbol', 'market', 'timeframe', 'timestamp', unique=True),
    )

    def __repr__(self):
        return f"<OHLCV {self.symbol} {self.timeframe} @ {self.timestamp}>"
