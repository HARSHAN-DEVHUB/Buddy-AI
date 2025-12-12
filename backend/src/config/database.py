"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/buddy_ai")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=int(os.getenv("DATABASE_POOL_SIZE", 5)),
    max_overflow=int(os.getenv("DATABASE_MAX_OVERFLOW", 10)),
    echo=os.getenv("DEBUG", "False").lower() == "true",  # Log SQL queries in debug mode
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db() -> Generator:
    """
    Database session dependency for FastAPI
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
