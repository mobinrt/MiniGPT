from fastapi import HTTPException, status, Depends, Query, Request, APIRouter
from typing import Optional

from src.app.user.schema import UserUpdate, UserCreate, UserDisplay
from src.app.user.controller import (
    create_user,
    get_user_by_id,
    get_user_by_email,
    delete_user,
    update_user,
)
from src.app.user.model import UserModel

from src.helpers.auth.rbac import role_required
from src.helpers.auth.dependencies import get_current_user
from src.helpers.auth import oauth2_scheme
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.exceptions.entities import DeleteAdmin

# from src.helpers.schema import UserResponseScheme
from src.helpers.filter import Filter
from src.helpers.pagination import Paginator, paginate_decorator
from src.helpers.order_by import OrderBy
from src.helpers.select import Select
from src.helpers.filter_schema import create_filter_schema
from src.helpers.enum.user_role import UserRole

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


UserFilterSchema = create_filter_schema(
    UserModel,
    excludes=["created_at", "updated_at", "password_hash", "pic_url", "is_admin"],
    filter_operations=["contains", "exact"],
)


@router.post(
    "/",
    response_model=UserDisplay,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"}},
)
async def create(data: UserCreate):
    try:
        new_user = await create_user(data.username, data.email, data.password)
        return UserDisplay.model_validate(new_user)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/",
    response_model=UserDisplay,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "User not found"}},
)
@role_required(UserRole.ADMIN.value)
async def read(
    id: Optional[int] = None,
    email: Optional[str] = None,
    token: str = Depends(oauth2_scheme),
):
    try:
        if id:
            user = await get_user_by_id(id)
        elif email:
            user = await get_user_by_email(email)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either id or email must be provided.",
            )
        return UserDisplay.model_validate(user)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/all/",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found any user"}},
)
@role_required(UserRole.ADMIN.value)
@paginate_decorator
async def read_all(
    request: Request,
    filters: UserFilterSchema = Depends(),  # type: ignore
    paginator: Paginator = Depends(),
    sort_by: list[str] = Query([]),
    select: list[str] = Query([]),
    token: str = Depends(oauth2_scheme),
):
    try:
        query = OrderBy.create(UserModel.all(), sort_by)

        filtered_query = Filter.create(query, filters)

        paginated_data = await paginator.paginate(filtered_query)

        selected_data = Select.create(
            paginated_data.paginated_result,
            select,
            UserModel,
            exclude=["password_hash"],
        )

        return await paginated_data.get_paginated_response(selected_data)
    except HTTPException as _e:
        if _e.status_code == 400:
            return {"error": _e.detail}
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/me/",
    response_model=UserDisplay,
    status_code=status.HTTP_200_OK,
)
@role_required(UserRole.MEMBER.value)
async def update_self(
    data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
):
    try:
        dict_data = data.model_dump()
        updated_user = await update_user(current_user.id, dict_data)
        return UserDisplay.model_validate(updated_user)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def delete(
    id: Optional[int] = None,
    current_user: UserModel = Depends(get_current_user),
):
    try:
        if id:
            if current_user.is_admin:
                await delete_user(id)
                return {"message": "User deleted successfully by admin"}
        else:
            await delete_user(user_id=current_user.id)
            return {"message": "Your account has been deleted successfully"}

        return {"message": "No action was taken"}
    except DeleteAdmin as ex:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=ex.message
        )
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
