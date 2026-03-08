"""
Tests for authentication endpoints (login, logout, protected routes).
"""

import pytest
from fastapi import status
from jose import jwt
from datetime import timedelta, datetime
from backend.app.core.security import SECRET_KEY, ALGORITHM
from backend.app.models.user import User, get_password_hash


def test_login_success(client, test_user):
    """Test successful login with valid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_user.email, "password": "testpass123"}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_login_invalid_email(client):
    """Test login with non-existent email."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent@example.com", "password": "testpass123"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "incorrect" in response.json()["detail"].lower()


def test_login_invalid_password(client, test_user):
    """Test login with wrong password."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_user.email, "password": "wrongpassword"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "incorrect" in response.json()["detail"].lower()


def test_get_current_user(client, auth_headers):
    """Test getting current user with valid token."""
    response = client.get("/api/v1/auth/me", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "email" in data
    assert "password" not in data
    assert "hashed_password" not in data


def test_get_current_user_unauthorized(client):
    """Test getting current user without token."""
    response = client.get("/api/v1/auth/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout_success(client, auth_headers):
    """Test successful logout."""
    response = client.post("/api/v1/auth/logout", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    assert "logged out" in response.json()["message"].lower()


def test_logout_without_token(client):
    """Test logout without token."""
    response = client.post("/api/v1/auth/logout")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_token_verification(client, auth_headers):
    """Test token verification endpoint."""
    response = client.get("/api/v1/auth/verify", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["authenticated"] is True
    assert "email" in data


def test_expired_token(client, db_session):
    """Test that expired tokens are rejected."""
    # Create test user
    user = User(
        email="expired@example.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Expired Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create expired token (expiration in the past)
    expire = datetime.utcnow() - timedelta(minutes=1)
    expired_payload = {
        "sub": user.email,
        "exp": expire
    }
    expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)

    # Try to access protected route with expired token
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )

    # Should return 401 with expired message
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "expired" in response.json()["detail"].lower()


def test_token_includes_user_id(client, db_session):
    """Verify that login tokens include user_id claim."""
    # Create test user
    user = User(
        email="tokenuser@example.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Token Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "tokenuser@example.com", "password": "testpass123"}
    )

    assert response.status_code == 200
    token = response.json()["access_token"]

    # Decode token and check for user_id
    from jose import jwt
    from backend.app.core.security import SECRET_KEY, ALGORITHM
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert "user_id" in payload
    assert payload["user_id"] == str(user.id)
    assert payload["sub"] == user.email


def test_get_user_id_from_token(client, db_session):
    """Verify get_user_id_from_token extracts user_id correctly."""
    from jose import jwt
    from backend.app.core.security import SECRET_KEY, ALGORITHM, create_access_token
    from backend.app.core.deps import get_user_id_from_token, credentials_exception

    # Create token with user_id
    test_user_id = "test-user-123"
    token = create_access_token(
        data={"sub": "test@example.com"},
        user_id=test_user_id
    )

    # Extract user_id
    extracted_id = get_user_id_from_token(token, credentials_exception)

    assert extracted_id == test_user_id
