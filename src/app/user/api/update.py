from fastapi import HTTPException, status, Depends
from . import router

from src.app.user.schema import UserDisplay, UserUpdate
from src.app.user.controller import update_user
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.auth.rbac import role_required
from src.helpers.enum.user_role import UserRole
from src.helpers.auth import oauth2_scheme
from src.helpers.auth.dependencies import get_current_user
from src.app.user.model import UserModel


@router.put(
    "/update/me",
    response_model=UserDisplay,
    status_code=status.HTTP_200_OK,
)
@role_required(UserRole.MEMBER.value)
async def update_user_self(
    data: UserUpdate,
    token: str = Depends(oauth2_scheme),
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
