"""
Prediction models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, JSON
from sqlalchemy.sql import func
from src.config.database import Base
import enum


class PredictionDirection(enum.Enum):
    """Prediction directions"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    STRONG_BUY = "STRONG_BUY"
    STRONG_SELL = "STRONG_SELL"


class ModelType(enum.Enum):
    """ML Model types"""
    TFT = "TFT"
    LSTM = "LSTM"
    ENSEMBLE = "ENSEMBLE"
    PROPHET = "PROPHET"
    MULTIMODAL = "MULTIMODAL"


class Prediction(Base):
    """Model for storing AI predictions"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    
    # User who requested the prediction
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    
    # Prediction details
    symbol = Column(String, index=True, nullable=False)
    market = Column(String, nullable=False)
    model = Column(Enum(ModelType), nullable=False)
    
    # Price predictions
    current_price = Column(Float, nullable=False)
    predicted_price = Column(Float, nullable=False)
    direction = Column(Enum(PredictionDirection), nullable=False)
    confidence = Column(Float, nullable=False)  # 0.0 to 1.0
    
    # Trading levels
    target_price = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    
    # Timeframe
    timeframe = Column(String, nullable=False)
    horizon_hours = Column(Integer, nullable=False)  # Prediction horizon in hours
    
    # Metadata
    features_used = Column(JSON, nullable=True)  # Features used for prediction
    model_version = Column(String, nullable=True)
    
    # Accuracy tracking
    actual_price = Column(Float, nullable=True)  # Actual price after horizon
    accuracy_score = Column(Float, nullable=True)  # How accurate was the prediction
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    prediction_for = Column(DateTime(timezone=True), nullable=False)  # When this prediction is for
    evaluated_at = Column(DateTime(timezone=True), nullable=True)  # When we checked accuracy

    def __repr__(self):
        return f"<Prediction {self.symbol} {self.direction} @ {self.confidence:.2f}>"
