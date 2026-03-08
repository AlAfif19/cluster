"""
Tests for user data isolation in user endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.app.main import app
from backend.app.core.security import get_password_hash
from backend.app.models.user import User
from backend.app.schemas.user import UserCreate
from backend.app.database import get_db


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    # In a real implementation, this would create a test database
    # For now, we'll use the database fixture from conftest
    pass


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def get_auth_headers(client: TestClient, user_email: str, password: str):
    """Helper function to get authentication headers."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": user_email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_user_cannot_access_other_users(client: TestClient, db_session: Session):
    """Verify users cannot access other users' data via email endpoint."""
    # Create two users
    user1 = User(email="user1@example.com", hashed_password=get_password_hash("pass123"), is_active=True)
    user2 = User(email="user2@example.com", hashed_password=get_password_hash("pass456"), is_active=True)
    db_session.add_all([user1, user2])
    db_session.commit()

    # Login as user1
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user1@example.com", "password": "pass123"}
    )
    token1 = response.json()["access_token"]

    # Try to access user2's email
    response = client.get(
        "/api/v1/users/email/user2@example.com",
        headers={"Authorization": f"Bearer {token1}"}
    )

    # Should return 403 Forbidden
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]


def test_get_users_returns_only_current_user(client: TestClient, db_session: Session):
    """Verify GET /users returns only the current authenticated user."""
    # Create multiple users
    user1 = User(email="user1@example.com", hashed_password=get_password_hash("pass123"), is_active=True)
    user2 = User(email="user2@example.com", hashed_password=get_password_hash("pass456"), is_active=True)
    db_session.add_all([user1, user2])
    db_session.commit()

    # Login as user1
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user1@example.com", "password": "pass123"}
    )
    token1 = response.json()["access_token"]

    # Get users
    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token1}"}
    )

    # Should return only user1
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["email"] == "user1@example.com"


def test_get_users_unauthenticated(client: TestClient):
    """Verify GET /users returns 401 when not authenticated."""
    response = client.get("/api/v1/users/")
    assert response.status_code == 401


def test_get_users_email_unauthenticated(client: TestClient):
    """Verify GET /users/email/{email} returns 401 when not authenticated."""
    response = client.get("/api/v1/users/email/user1@example.com")
    assert response.status_code == 401


def test_get_users_email_not_found(client: TestClient, db_session: Session):
    """Verify GET /users/email/{email} returns 404 when user doesn't exist."""
    # Create a user
    user = User(email="user1@example.com", hashed_password=get_password_hash("pass123"), is_active=True)
    db_session.add(user)
    db_session.commit()

    # Login as user1
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user1@example.com", "password": "pass123"}
    )
    token1 = response.json()["access_token"]

    # Try to access non-existent user's email
    response = client.get(
        "/api/v1/users/email/nonexistent@example.com",
        headers={"Authorization": f"Bearer {token1}"}
    )

    # Should return 404
    assert response.status_code == 404


def test_user_can_access_own_email(client: TestClient, db_session: Session):
    """Verify users can access their own email profile."""
    # Create a user
    user = User(email="user1@example.com", hashed_password=get_password_hash("pass123"), is_active=True)
    db_session.add(user)
    db_session.commit()

    # Login as user1
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user1@example.com", "password": "pass123"}
    )
    token1 = response.json()["access_token"]

    # Access own email
    response = client.get(
        "/api/v1/users/email/user1@example.com",
        headers={"Authorization": f"Bearer {token1}"}
    )

    # Should return 200 with user data
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["email"] == "user1@example.com"


def test_inactive_user_cannot_access_data(client: TestClient, db_session: Session):
    """Verify inactive users cannot access data."""
    # Create an inactive user
    user = User(email="user1@example.com", hashed_password=get_password_hash("pass123"), is_active=False)
    db_session.add(user)
    db_session.commit()

    # Try to login with inactive user
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "user1@example.com", "password": "pass123"}
    )

    # Should return 400 Bad Request (inactive user)
    assert response.status_code == 400


# Additional tests for isolation patterns
def test_isolation_enforcement_integration(client: TestClient, db_session: Session):
    """Integration test for complete isolation enforcement."""
    # Create three users
    users = [
        User(email="alice@example.com", hashed_password=get_password_hash("pass1"), is_active=True),
        User(email="bob@example.com", hashed_password=get_password_hash("pass2"), is_active=True),
        User(email="charlie@example.com", hashed_password=get_password_hash("pass3"), is_active=True)
    ]
    db_session.add_all(users)
    db_session.commit()

    # Login as alice
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "alice@example.com", "password": "pass1"}
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Get users - should only see alice
    response = client.get("/api/v1/users/", headers=headers)
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["email"] == "alice@example.com"

    # Try to access bob's email - should be denied
    response = client.get("/api/v1/users/email/bob@example.com", headers=headers)
    assert response.status_code == 403

    # Try to access charlie's email - should be denied
    response = client.get("/api/v1/users/email/charlie@example.com", headers=headers)
    assert response.status_code == 403

    # Access own email - should be allowed
    response = client.get("/api/v1/users/email/alice@example.com", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"