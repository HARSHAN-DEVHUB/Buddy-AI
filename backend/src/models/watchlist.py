"""
Watchlist and alert models
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from src.config.database import Base
import enum


class AlertType(enum.Enum):
    """Alert types"""
    PRICE = "price"
    PREDICTION = "prediction"
    INDICATOR = "indicator"


class AlertCondition(enum.Enum):
    """Alert trigger conditions"""
    ABOVE = "above"
    BELOW = "below"
    CROSS = "cross"


class Watchlist(Base):
    """Model for user watchlists"""
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Symbol details
    symbol = Column(String, nullable=False)
    market = Column(String, nullable=False)
    
    # User notes
    notes = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Watchlist {self.symbol} for User {self.user_id}>"


class Alert(Base):
    """Model for price alerts"""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Alert details
    symbol = Column(String, nullable=False, index=True)
    alert_type = Column(Enum(AlertType), nullable=False)
    condition = Column(Enum(AlertCondition), nullable=False)
    target_value = Column(Float, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_triggered = Column(Boolean, default=False, nullable=False)
    
    # Message
    message = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    triggered_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Alert {self.symbol} {self.condition.value} {self.target_value}>"


class Position(Base):
    """Model for tracking user positions (virtual trading)"""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Position details
    symbol = Column(String, nullable=False)
    market = Column(String, nullable=False)
    side = Column(String, nullable=False)  # long or short
    
    # Prices
    entry_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=True)
    exit_price = Column(Float, nullable=True)
    
    # Quantity
    quantity = Column(Float, nullable=False)
    
    # P&L
    pnl = Column(Float, nullable=True)
    pnl_percent = Column(Float, nullable=True)
    
    # Status
    is_open = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    opened_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    closed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Position {self.symbol} {self.side} @ {self.entry_price}>"
