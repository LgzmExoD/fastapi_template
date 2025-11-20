"""
Authentication endpoints for login, logout, and token management.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from app.api import deps
from app.core import security
from app.core.config import settings
from app.db.repositories.token_blacklist import (TokenBlacklistCreate,
                                                 token_blacklist)
from app.db.repositories.user import user as user_repo
from app.schemas.token import Token
from app.schemas.user import User

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login(
    db: deps.SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Any:
    """
    OAuth2 compatible token login.

    Get an access token and refresh token for future requests.
    """
    user = await user_repo.authenticate(
        db, email=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return {
        "access_token": security.create_access_token(
            user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    token: deps.TokenDep,
    db: deps.SessionDep,
    current_user: deps.CurrentUser,
) -> dict:
    """
    Logout by blacklisting the current token.

    The token will be invalid for future requests.
    """
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

    await token_blacklist.create(
        db, data=TokenBlacklistCreate(token=token, expires_at=expires_at)
    )

    return {"message": "Successfully logged out"}


@router.get("/login/test-token", response_model=User)
async def test_token(current_user: deps.CurrentUser) -> Any:
    """
    Test access token validity.

    Returns the current user if token is valid.
    """
    return current_user
