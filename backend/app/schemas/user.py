"""
Pydantic schemas for user validation and serialization.

This module defines the request and response schemas for user operations,
ensuring data validation and proper serialization between API layers.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base fields shared between user schemas."""
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """
    Schema for user registration/creation requests.

    Attributes:
        email: User's email address (validated as email format)
        full_name: User's full name (optional)
        password: Plain text password (min 8 characters)
    """
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserLogin(BaseModel):
    """
    Schema for user login requests.

    Attributes:
        email: User's email address
        password: Plain text password
    """
    email: EmailStr
    password: str


class User(UserBase):
    """
    Schema for user response serialization.

    Attributes:
        id: User's UUID
        email: User's email address
        full_name: User's full name (optional)
        is_active: Whether the user account is active
        created_at: Timestamp when user was created

    Note: This schema excludes password and hashed_password fields.
    """
    id: str
    is_active: bool
    created_at: datetime

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True  # For Pydantic v2, replaces orm_mode


class Token(BaseModel):
    """
    Schema for token response.

    Attributes:
        access_token: JWT access token
        token_type: Type of token (typically "bearer")
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token payload data.

    Attributes:
        email: User's email (optional, for token validation)
    """
    email: Optional[str] = None
