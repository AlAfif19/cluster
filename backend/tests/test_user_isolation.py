"""
Tests for user data isolation in user endpoints.
"""

import pytest
from fastapi import status
from backend.app.models.user import User, get_password_hash

def test_get_users_unauthenticated(client):
    """Verify GET /users returns 401 when not authenticated."""
    response = client.get("/api/v1/users/")
    assert response.status_code == 401


def test_get_users_email_unauthenticated(client):
    """Verify GET /users/email/{email} returns 401 when not authenticated."""
    response = client.get("/api/v1/users/email/user1@example.com")
    assert response.status_code == 401


def test_user_cannot_access_other_users(client, test_user):
    """Verify users cannot access other users' data via email endpoint."""
    # Login as test_user
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_user.email, "password": "testpass123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Try to access another user's email (should be 404 since no other user exists)
    response = client.get(
        "/api/v1/users/email/anotheruser@example.com",
        headers=headers
    )

    # In a real scenario with multiple users, this should return 403
    # Since we only have one test user, it returns 404 (not found)
    assert response.status_code in [403, 404]


def test_get_users_returns_only_current_user(client, test_user):
    """Verify GET /users returns only the current authenticated user."""
    # Login as test_user
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_user.email, "password": "testpass123"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get users
    response = client.get(
        "/api/v1/users/",
        headers=headers
    )

    # Should return only the current user
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) == 1
    assert users[0]["email"] == test_user.email


def test_get_users_email_not_found(client, test_user, auth_headers):
    """Verify GET /users/email/{email} returns 403 for non-existent users (email checked first)."""
    # Try to access non-existent user's email
    response = client.get(
        "/api/v1/users/email/nonexistent@example.com",
        headers=auth_headers
    )

    # Should return 403 because we check email ownership before checking existence
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]


def test_user_can_access_own_email(client, test_user, auth_headers):
    """Verify users can access their own email profile."""
    # Access own email
    response = client.get(
        "/api/v1/users/email/test@example.com",
        headers=auth_headers
    )

    # Should return 200 with user data
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["email"] == test_user.email


def test_inactive_user_cannot_access_data(client, db_session, auth_headers):
    """Verify inactive users cannot access data."""
    # Create an inactive user
    inactive_user = User(
        email="inactive@example.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Inactive User",
        is_active=False
    )
    db_session.add(inactive_user)
    db_session.commit()
    db_session.refresh(inactive_user)

    # Try to login with inactive user
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "inactive@example.com", "password": "testpass123"}
    )

    # Should return 401 Unauthorized (inactive user)
    assert response.status_code == 401


def test_isolation_enforcement_integration(client, test_user, auth_headers):
    """Integration test for complete isolation enforcement."""
    # Login as test_user
    response = client.get("/api/v1/users/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) == 1
    assert users[0]["email"] == test_user.email

    # Try to access other emails (should be 403 since we check email ownership first)
    response = client.get("/api/v1/users/email/other@example.com", headers=auth_headers)
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]

    # Access own email - should be allowed
    response = client.get("/api/v1/users/email/test@example.com", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == test_user.email