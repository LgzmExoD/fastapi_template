"""
Pydantic schemas for analytics and metrics responses.
"""

from pydantic import BaseModel, Field


class SystemMetrics(BaseModel):
    """Overall system metrics."""

    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    inactive_users: int = Field(..., description="Number of inactive users")
    total_tenants: int = Field(..., description="Total number of tenants")
    active_tenants: int = Field(..., description="Number of active tenants")
    inactive_tenants: int = Field(..., description="Number of inactive tenants")


class UserMetrics(BaseModel):
    """Detailed user metrics."""

    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    inactive_users: int = Field(..., description="Number of inactive users")
    superadmins: int = Field(..., description="Number of superadmin users")
    admins: int = Field(..., description="Number of admin users")
    regular_users: int = Field(..., description="Number of regular users")
    average_users_per_tenant: float = Field(..., description="Average users per tenant")


class TenantMetrics(BaseModel):
    """Detailed tenant metrics."""

    total_tenants: int = Field(..., description="Total number of tenants")
    active_tenants: int = Field(..., description="Number of active tenants")
    inactive_tenants: int = Field(..., description="Number of inactive tenants")
    tenants_with_users: int = Field(..., description="Tenants that have users")
    tenants_without_users: int = Field(..., description="Tenants without users")
    min_users_per_tenant: int = Field(..., description="Minimum users in a tenant")
    max_users_per_tenant: int = Field(..., description="Maximum users in a tenant")
    avg_users_per_tenant: float = Field(..., description="Average users per tenant")


class ActivityMetrics(BaseModel):
    """Activity and engagement metrics."""

    period_days: int = Field(..., description="Analysis period in days")
    total_logins: int = Field(..., description="Total login events")
    unique_active_users: int = Field(..., description="Unique active users")
    average_logins_per_day: float = Field(..., description="Average logins per day")
    peak_concurrent_users: int = Field(..., description="Peak concurrent users")
