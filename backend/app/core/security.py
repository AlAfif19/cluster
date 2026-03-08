"""
JWT token security utilities with expiration handling.

This module provides JWT token creation, verification, and expiration handling
for secure authentication in the FastAPI application.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, ExpiredSignatureError, jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
import os

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Read from environment or default to 30 minutes
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-must-be-changed")
ALGORITHM = "HS256"


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token with expiration.

    Args:
        data: Data to encode in the token (typically user info)
        expires_delta: Optional custom expiration time

    Returns:
        JWT access token string
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception) -> str:
    """
    Decode JWT token and validate expiration.
    Raises credentials_exception if token is invalid or expired.

    Args:
        token: JWT token to verify
        credentials_exception: Exception to raise if validation fails

    Returns:
        Decoded token payload (typically user email)
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        return email

    except ExpiredSignatureError:
        # Token has expired
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        # Invalid token (signature, format, etc.)
        raise credentials_exception


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


# Token blacklist for logout functionality
token_blacklist = set()

# OAuth2 scheme for Bearer token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Create credentials exception for reuse
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_token_signature(token: str) -> str:
    """
    Extract token signature for blacklist (first 64 chars of token).
    Using token prefix as signature is sufficient for v1.
    """
    import hashlib
    return hashlib.sha256(token.encode()).hexdigest()[:64]


def invalidate_token(token: str) -> bool:
    """
    Add token to blacklist.
    Returns True if token was successfully invalidated.
    """
    try:
        signature = get_token_signature(token)
        token_blacklist.add(signature)
        return True
    except Exception as e:
        return False


def is_token_blacklisted(token: str) -> bool:
    """
    Check if token is in blacklist.
    Returns True if token is blacklisted (invalid).
    """
    try:
        signature = get_token_signature(token)
        return signature in token_blacklist
    except Exception as e:
        return True  # Treat errors as blacklisted for security


def clear_blacklisted_token(token: str) -> bool:
    """
    Remove token from blacklist (for testing or manual cleanup).
    Returns True if token was removed.
    """
    try:
        signature = get_token_signature(token)
        if signature in token_blacklist:
            token_blacklist.remove(signature)
            return True
        return False
    except Exception as e:
        return False