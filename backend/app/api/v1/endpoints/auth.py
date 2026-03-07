"""
Authentication endpoints including login and protected routes.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.schemas.user import Token, User as UserSchema
from backend.app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.app.core.deps import get_current_active_user

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login with email and password to get JWT access token.
    """
    # Find user by email (OAuth2PasswordRequestForm uses username field for email)
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user information.
    """
    return current_user


@router.post("/logout")
def logout(current_user: User = Depends(get_current_active_user)):
    """
    Logout endpoint (client-side token invalidation).
    """
    return {"message": "Successfully logged out"}


@router.get("/verify")
def verify_token_status(current_user: User = Depends(get_current_active_user)):
    """
    Verify current token and return user status.
    """
    return {
        "authenticated": True,
        "email": current_user.email,
        "is_active": current_user.is_active
    }