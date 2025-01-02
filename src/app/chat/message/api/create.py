from fastapi import HTTPException, status
from . import router

from src.app.user.schema import UserCreate, UserDisplay
from src.app.user.controller import create_user
from src.helpers.exceptions.base_exception import BaseError


@router.post(
    "/create",
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
