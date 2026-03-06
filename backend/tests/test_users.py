"""
Tests for user registration endpoint.
"""

import pytest
from fastapi import status


def test_register_user(client):
    """Test successful user registration."""
    response = client.post(
        "/api/v1/users/register",
        json={
            "email": "newuser@example.com",
            "password": "newpass123",
            "full_name": "New User"
        }
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user):
    """Test that duplicate email returns 400 error."""
    response = client.post(
        "/api/v1/users/register",
        json={
            "email": test_user.email,
            "password": "anotherpass123",
            "full_name": "Another User"
        }
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already registered" in response.json()["detail"].lower()


def test_register_invalid_email(client):
    """Test that invalid email format is rejected."""
    response = client.post(
        "/api/v1/users/register",
        json={
            "email": "not-an-email",
            "password": "testpass123",
            "full_name": "Test User"
        }
    )

    # Should return 422 (validation error)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_register_short_password(client):
    """Test that short password is rejected."""
    response = client.post(
        "/api/v1/users/register",
        json={
            "email": "short@example.com",
            "password": "short",
            "full_name": "Short User"
        }
    )

    # Should return 422 (validation error)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_list_users(client, test_user):
    """Test listing all users."""
    response = client.get("/api/v1/users/")

    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) >= 1
    assert any(u["email"] == test_user.email for u in users)
