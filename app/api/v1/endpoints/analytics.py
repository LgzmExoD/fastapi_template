"""
Analytics and metrics endpoints for system monitoring.
"""

from typing import Any

from fastapi import APIRouter
from sqlalchemy import func, select

from app.api import deps
from app.models.tenant import Tenant
from app.models.user import User, UserRole
from app.schemas.analytics import (ActivityMetrics, SystemMetrics,
                                   TenantMetrics, UserMetrics)

router = APIRouter()


@router.get("/system", response_model=SystemMetrics)
async def get_system_metrics(
    db: deps.SessionDep,
    current_user: deps.CurrentUser,
) -> Any:
    """
    Retrieve system-wide statistics.

    Provides a high-level overview of total users, tenants, and their active status.
    """
    # Total users
    total_users = await db.scalar(select(func.count(User.id)))

    # Active users
    active_users = await db.scalar(select(func.count(User.id)).where(User.is_active))

    # Total tenants
    total_tenants = await db.scalar(select(func.count(Tenant.id)))

    # Active tenants
    active_tenants = await db.scalar(
        select(func.count(Tenant.id)).where(Tenant.is_active)
    )

    return {
        "total_users": total_users or 0,
        "active_users": active_users or 0,
        "inactive_users": (total_users or 0) - (active_users or 0),
        "total_tenants": total_tenants or 0,
        "active_tenants": active_tenants or 0,
        "inactive_tenants": (total_tenants or 0) - (active_tenants or 0),
    }


@router.get("/users", response_model=UserMetrics)
async def get_user_metrics(
    db: deps.SessionDep,
    current_user: deps.CurrentUser,
) -> Any:
    """
    Retrieve detailed user statistics.

    Breaks down user data by role (admin, regular user, etc.) and activity levels.
    """
    # Users by role
    role_counts = await db.execute(
        select(User.role, func.count(User.id)).group_by(User.role)
    )

    users_by_role = {role: count for role, count in role_counts.all()}

    # Total and active users
    total_users = await db.scalar(select(func.count(User.id)))
    active_users = await db.scalar(select(func.count(User.id)).where(User.is_active))

    # Average users per tenant
    users_per_tenant = await db.execute(
        select(User.tenant_id, func.count(User.id).label("user_count"))
        .where(User.tenant_id.isnot(None))
        .group_by(User.tenant_id)
    )

    tenant_user_counts = [count for _, count in users_per_tenant.all()]
    avg_users_per_tenant = (
        sum(tenant_user_counts) / len(tenant_user_counts) if tenant_user_counts else 0
    )

    return {
        "total_users": total_users or 0,
        "active_users": active_users or 0,
        "inactive_users": (total_users or 0) - (active_users or 0),
        "superadmins": users_by_role.get(UserRole.SUPERADMIN.value, 0),
        "admins": users_by_role.get(UserRole.ADMIN.value, 0),
        "regular_users": users_by_role.get(UserRole.USER.value, 0),
        "average_users_per_tenant": round(avg_users_per_tenant, 2),
    }


@router.get("/tenants", response_model=TenantMetrics)
async def get_tenant_metrics(
    db: deps.SessionDep,
    current_user: deps.CurrentUser,
) -> Any:
    """
    Get detailed tenant metrics.

    Returns tenant statistics and distribution.
    """
    # Total and active tenants
    total_tenants = await db.scalar(select(func.count(Tenant.id)))
    active_tenants = await db.scalar(
        select(func.count(Tenant.id)).where(Tenant.is_active)
    )

    # Tenants with users
    tenants_with_users = await db.scalar(
        select(func.count(func.distinct(User.tenant_id))).where(
            User.tenant_id.isnot(None)
        )
    )

    # Users per tenant distribution
    users_per_tenant = await db.execute(
        select(User.tenant_id, func.count(User.id).label("user_count"))
        .where(User.tenant_id.isnot(None))
        .group_by(User.tenant_id)
    )

    tenant_user_counts = [count for _, count in users_per_tenant.all()]

    return {
        "total_tenants": total_tenants or 0,
        "active_tenants": active_tenants or 0,
        "inactive_tenants": (total_tenants or 0) - (active_tenants or 0),
        "tenants_with_users": tenants_with_users or 0,
        "tenants_without_users": (total_tenants or 0) - (tenants_with_users or 0),
        "min_users_per_tenant": min(tenant_user_counts) if tenant_user_counts else 0,
        "max_users_per_tenant": max(tenant_user_counts) if tenant_user_counts else 0,
        "avg_users_per_tenant": (
            round(sum(tenant_user_counts) / len(tenant_user_counts), 2)
            if tenant_user_counts
            else 0
        ),
    }


@router.get("/activity", response_model=ActivityMetrics)
async def get_activity_metrics(
    db: deps.SessionDep,
    current_user: deps.CurrentUser,
    days: int = 30,
) -> Any:
    """
    Get activity metrics for the specified period.

    Args:
        days: Number of days to analyze (default: 30)

    Returns activity statistics.
    """
    # This is a placeholder - you would track actual login/activity data
    # For now, returning mock structure

    return {
        "period_days": days,
        "total_logins": 0,  # Implement login tracking
        "unique_active_users": 0,  # Implement activity tracking
        "average_logins_per_day": 0.0,
        "peak_concurrent_users": 0,
    }
