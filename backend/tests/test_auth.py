"""
Tests for authentication endpoints (login, logout, protected routes).
"""

import pytest
from fastapi import status


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


def test_expired_token(client):
    """Test that expired tokens are rejected."""
    # This test will be implemented in Plan 02-07
    pytest.skip("Expired token testing implemented in Plan 02-07")
