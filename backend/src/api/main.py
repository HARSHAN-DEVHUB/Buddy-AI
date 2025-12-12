"""
Main FastAPI application
AI-Powered Market Prediction Platform
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database dependencies
from src.config.database import get_db, engine
from src.models import Base

# Create tables (in production, use alembic migrations)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Buddy AI API",
    description="AI-Powered Market Prediction Platform",
    version="1.0.0"
)

# CORS middleware
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Buddy AI API",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint with database connection test"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

# Placeholder routes - will be implemented later
@app.get("/api/market/price/{market}/{symbol}")
async def get_price(market: str, symbol: str, db: Session = Depends(get_db)):
    return {
        "success": True,
        "data": {
            "symbol": symbol,
            "market": market,
            "price": 0,
            "change24h": 0,
            "changePercent24h": 0,
            "high24h": 0,
            "low24h": 0,
            "volume24h": 0,
            "lastUpdate": 0
        }
    }

@app.get("/api/market/overview/{market}")
async def get_market_overview(market: str, db: Session = Depends(get_db)):
    return {
        "success": True,
        "data": {
            "totalVolume": 0,
            "avgChange": 0,
            "topGainers": [],
            "topLosers": [],
            "mostActive": []
        }
    }

@app.post("/api/prediction/predict")
async def create_prediction(db: Session = Depends(get_db)):
    return {
        "success": True,
        "data": {
            "id": "pred_1",
            "symbol": "XAUUSD",
            "market": "forex",
            "currentPrice": 2000,
            "predictedPrice": 2050,
            "direction": "BUY",
            "confidence": 0.75,
            "targetPrice": 2100,
            "stopLoss": 1950,
            "takeProfit": 2100,
            "timeframe": "1h",
            "horizon": 24,
            "timestamp": 0,
            "model": "TFT"
        }
    }

