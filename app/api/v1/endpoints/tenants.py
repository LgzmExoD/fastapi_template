"""
Tenant management endpoints for multitenancy administration.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import deps
from app.db.repositories.tenant import tenant as tenant_repo
from app.models.user import User
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate

router = APIRouter()


@router.get("/", response_model=list[Tenant])
async def list_tenants(
    db: deps.SessionDep,
    current_user: Annotated[User, Depends(deps.get_current_superuser)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve list of tenants.

    Requires superuser privileges.
    """
    return await tenant_repo.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=Tenant, status_code=status.HTTP_201_CREATED)
async def create_tenant(
    db: deps.SessionDep,
    tenant_in: TenantCreate,
    current_user: Annotated[User, Depends(deps.get_current_superuser)],
) -> Any:
    """
    Create new tenant.

    Requires superuser privileges.
    """
    return await tenant_repo.create(db, data=tenant_in)


@router.get("/{tenant_id}", response_model=Tenant)
async def get_tenant(
    tenant_id: int,
    db: deps.SessionDep,
    current_user: Annotated[User, Depends(deps.get_current_superuser)],
) -> Any:
    """
    Get tenant by ID.

    Requires superuser privileges.
    """
    tenant = await tenant_repo.get(db, id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found"
        )
    return tenant


@router.put("/{tenant_id}", response_model=Tenant)
async def update_tenant(
    tenant_id: int,
    tenant_in: TenantUpdate,
    db: deps.SessionDep,
    current_user: Annotated[User, Depends(deps.get_current_superuser)],
) -> Any:
    """
    Update tenant by ID.

    Requires superuser privileges.
    """
    tenant = await tenant_repo.get(db, id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found"
        )
    return await tenant_repo.update(db, instance=tenant, data=tenant_in)
