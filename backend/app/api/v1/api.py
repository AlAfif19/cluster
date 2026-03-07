"""
API router aggregation for version 1 endpoints.
"""

from fastapi import APIRouter

from backend.app.api.v1.endpoints.users import router as users_router
from backend.app.api.v1.endpoints.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])