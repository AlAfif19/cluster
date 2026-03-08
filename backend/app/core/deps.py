"""
Authentication dependencies for protected routes.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.core.security import verify_token, oauth2_scheme, is_token_blacklisted

# Credentials exception for unauthorized access
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Ownership exception for forbidden access
ownership_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to access this resource",
)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Verify JWT token, check blacklist, and return current user.
    """
    # Verify token and extract email
    email = verify_token(token, credentials_exception)

    # Check if token is blacklisted (logged out)
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been invalidated (user logged out)",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
        # Check if token is blacklisted first
        if is_token_blacklisted(token):
            return None

        email = verify_token(token, credentials_exception)
        user = db.query(User).filter(User.email == email).first()
        return user if user else None
    except HTTPException:
        return None


def require_user_ownership(user_id: str, current_user: User = Depends(get_current_active_user)) -> User:
    """
    Verify that current_user owns the resource with user_id.
    Raises 403 if user_id doesn't match current_user.id.
    Use this as a dependency in endpoints that access user-specific resources.
    """
    if current_user.id != user_id:
        raise ownership_exception
    return current_user


def optional_user_ownership(user_id: str, current_user: User = Depends(get_current_user_optional)) -> User | None:
    """
    Verify ownership if user is authenticated.
    Returns None if not authenticated (for public endpoints).
    Raises 403 if authenticated but not owner.
    """
    if current_user is None:
        return None
    if current_user.id != user_id:
        raise ownership_exception
    return current_user


def get_user_id_from_token(token: str = Depends(oauth2_scheme)) -> str:
    """
    Extract user_id from JWT token without database lookup.
    Useful for filtering queries by user_id.
    Raises 401 if token is invalid or blacklisted.
    """
    email = verify_token(token, credentials_exception)

    # Check blacklist
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been invalidated (user logged out)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Note: We can't get user_id from token without DB lookup in current implementation
    # This helper is for future enhancement when user_id is included in JWT
    # For now, this function is a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User ID extraction from token not yet implemented"
    )


__all__ = [
    "get_current_user",
    "get_current_active_user",
    "get_current_user_optional",
    "require_user_ownership",
    "optional_user_ownership",
]