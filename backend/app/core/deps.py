"""
Authentication dependencies for protected routes.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.core.security import verify_token, oauth2_scheme

# Credentials exception for unauthorized access
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Verify JWT token and return current user.
    """
    # Verify token and extract email
    email = verify_token(token, credentials_exception)

    # Query user from database
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get current active user (user must be active).
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_user_optional(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    """
    Verify JWT token and return current user if token provided, None otherwise.
    Returns None instead of raising exception for optional auth.
    """
    try:
        email = verify_token(token, credentials_exception)
        user = db.query(User).filter(User.email == email).first()
        return user if user else None
    except HTTPException:
        return None