from fastapi import HTTPException, status, Depends
from typing import Sequence

from . import router
from src.app.user.schema import UserDisplay
from src.app.user.controller import get_user_by_id, get_user_by_email, get_users
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.auth.rbac import role_required
from src.helpers.enum.user_role import UserRole
from src.helpers.auth.controller import oauth2_scheme


@router.get(
    "/{id}",
    response_model=UserDisplay,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "User not found"}},
)
@role_required(UserRole.ADMIN.value)
async def find_user_by_id(
    id: int,
    token: str = Depends(oauth2_scheme),
):
    try:
        user = await get_user_by_id(id)
        return UserDisplay.model_validate(user)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/by/{email}",
    response_model=UserDisplay,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "User not found"}},
)
@role_required(UserRole.ADMIN.value)
async def find_user_by_email(
    email: str,
    token: str = Depends(oauth2_scheme),
):
    try:
        user = await get_user_by_email(email)
        return UserDisplay.model_validate(user)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/",
    response_model=Sequence[UserDisplay],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found any user"}},
)
@role_required(UserRole.ADMIN.value)
async def find_users(
    token: str = Depends(oauth2_scheme),
):
    try:
        users = await get_users()
        return UserDisplay.model_validate(users)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
