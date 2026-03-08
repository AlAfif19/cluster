"""
Database connection and session management for SQLAlchemy.

This module provides the database engine, session factory, and dependency
injection function for use with FastAPI endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://kmeans_user:your_password_here@db:3306/kmeans_db")

# Create SQLAlchemy engine with MySQL-specific settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False           # Set to True for SQL query logging in development
)

# Create declarative base for model definitions
Base = declarative_base()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency function that provides a database session.

    Yields a database session and ensures it's closed after use.
    This is designed to be used as a FastAPI dependency injection.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables.

    This function should be called during application startup to ensure
    all tables defined in the models are created in the database.
    """
    # Import all models here to ensure they're registered with Base
    from backend.app.models import user  # noqa: F401

    # Create all tables
    Base.metadata.create_all(bind=engine)
