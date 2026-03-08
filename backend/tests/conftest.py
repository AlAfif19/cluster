"""
Pytest configuration and fixtures for authentication tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.database import get_db, Base
from backend.app.models.user import User, get_password_hash


# Create test database engine (uses in-memory SQLite for speed)
# For MySQL tests, use a separate test database
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database session for each test.
    All changes are rolled back after the test.
    """
    # Create tables
    Base.metadata.create_all(bind=test_engine)

    # Create session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        # Rollback and cleanup
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session: Session):
    """
    Create a test client with database override.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db_session: Session):
    """
    Create a test user in the database.
    Returns the user object.
    """
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        full_name="Test User",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_user_token(client, test_user):
    """
    Create a test user and return JWT token.
    Useful for testing authenticated endpoints.
    """
    response = client.post(
        "/api/v1/auth/login",
        data={"username": test_user.email, "password": "testpass123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def auth_headers(test_user_token):
    """
    Return authorization headers with JWT token.
    """
    return {"Authorization": f"Bearer {test_user_token}"}
