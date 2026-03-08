"""
User SQLAlchemy model with password hashing utilities.

This module defines the User model for the database and provides
password hashing and verification functions using bcrypt.
"""

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.mysql import CHAR as UUID
from passlib.context import CryptContext
from datetime import datetime
import uuid

# Import Base from database
from backend.app.database import Base

# Create password hashing context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The bcrypt hashed password to compare against

    Returns:
        True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: The plain text password to hash

    Returns:
        The bcrypt hashed password
    """
    return pwd_context.hash(password)


class User(Base):
    """
    User model representing a user account in the database.

    Attributes:
        id: UUID primary key for the user
        email: Unique email address (indexed for fast lookups)
        hashed_password: Bcrypt hashed password (never plain text)
        full_name: User's full name (optional)
        is_active: Whether the user account is active
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    __tablename__ = "users"

    id = Column(UUID(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        """String representation of User for debugging."""
        return f"<User(id={self.id}, email={self.email}, is_active={self.is_active})>"
