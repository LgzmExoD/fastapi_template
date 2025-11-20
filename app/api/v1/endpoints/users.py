"""
User management endpoints.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.api import deps
from app.db.repositories.user import user as user_repo
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=list[User])
async def list_users(
    db: deps.SessionDep,
    current_user: Annotated[User, Depends(deps.get_current_superuser)],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve list of users.

    Requires superuser privileges.
    """
    return await user_repo.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    db: deps.SessionDep,
    user_in: UserCreate,
    current_user: Annotated[User, Depends(deps.get_current_superuser)],
) -> Any:
    """
    Create new user.

    Requires superuser privileges.
    """
    existing_user = await user_repo.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    return await user_repo.create(db, data=user_in)


@router.get("/me", response_model=User)
async def get_current_user(
    current_user: Annotated[User, Depends(deps.get_current_active_user)],
) -> Any:
    """
    Get current authenticated user.
    """
    return current_user


@router.put("/me", response_model=User)
async def update_current_user(
    db: deps.SessionDep,
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(deps.get_current_active_user)],
) -> Any:
    """
    Update current user profile.
    """
    return await user_repo.update(db, instance=current_user, data=user_in)


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: deps.SessionDep,
    current_user: Annotated[User, Depends(deps.get_current_active_user)],
) -> Any:
    """
    Get user by ID.

    Users can only access their own profile unless they are superadmin.
    """
    user = await user_repo.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if user.id != current_user.id and current_user.role != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges"
        )

    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: deps.SessionDep,
    current_user: Annotated[User, Depends(deps.get_current_superuser)],
) -> Any:
    """
    Update user by ID.

    Requires superuser privileges.
    """
    user = await user_repo.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return await user_repo.update(db, instance=user, data=user_in)
