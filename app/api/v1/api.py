"""
API v1 router aggregation.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import analytics, dashboard, login, tenants, users

api_router = APIRouter()

# Authentication endpoints
api_router.include_router(login.router, tags=["Authentication"])

# User management endpoints
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# Tenant management endpoints
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])

# Analytics and metrics endpoints
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])

# Visual Dashboard
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
