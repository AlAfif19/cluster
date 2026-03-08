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
from backend.app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, invalidate_token, is_token_blacklisted, oauth2_scheme
from backend.app.core.deps import get_current_active_user, get_current_user

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

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        user_id=str(user.id),  # Include user_id in token
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserSchema)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user information.
    """
    return current_user


@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    """
    Logout current user by invalidating JWT token.
    """
    success = invalidate_token(token)
    if success:
        return {"message": "Successfully logged out"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to logout"
        )


@router.post("/logout-all")
def logout_all(current_user: User = Depends(get_current_active_user)):
    """
    Logout all sessions for current user by blacklisting all tokens.
    Note: In v1 with simple blacklist, this clears the entire blacklist.
    For production, implement user-specific token tracking.
    """
    # For v1: Clear entire blacklist (all tokens)
    from backend.app.core.security import token_blacklist
    token_blacklist.clear()
    return {"message": "All sessions logged out"}


@router.get("/logout-status")
def logout_status(token: str = Depends(oauth2_scheme)):
    """
    Check if current token has been logged out.
    """
    is_blacklisted = is_token_blacklisted(token)
    return {
        "logged_out": is_blacklisted,
        "message": "Token is valid" if not is_blacklisted else "Token has been invalidated"
    }


@router.get("/verify")
def verify_token_status(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Verify current token and return user status.
    """

    if is_token_blacklisted(token):
        return {
            "authenticated": False,
            "logged_out": True,
            "message": "Token has been invalidated"
        }

    user = get_current_user(token, db)
    return {
        "authenticated": True,
        "logged_out": False,
        "email": user.email,
        "is_active": user.is_active
    }