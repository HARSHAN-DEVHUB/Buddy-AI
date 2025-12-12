"""
User model for authentication and user management
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from src.config.database import Base
import enum


class UserRole(enum.Enum):
    """User roles for authorization"""
    USER = "user"
    ADMIN = "admin"
    PREMIUM = "premium"


class User(Base):
    """User model for storing user account information"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # User details
    full_name = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Preferences
    preferred_currency = Column(String, default="USD", nullable=False)
    preferred_theme = Column(String, default="dark", nullable=False)
    enable_notifications = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"
