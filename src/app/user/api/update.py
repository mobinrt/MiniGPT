from fastapi import HTTPException, status, Depends
from . import router

from src.app.user.schema import UserDisplay, UserUpdate
from src.app.user.controller import update_user
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.auth.rbac import role_required, check_role
from src.helpers.enum.user_role import UserRole
from src.helpers.auth.controller import oauth2_scheme, AuthController
from src.helpers.auth.dependencies import get_auth_controller


@router.put(
    "/update/me",
    response_model=UserDisplay,
    status_code=status.HTTP_200_OK,
)
@role_required(UserRole.MEMBER.value)
async def delete_user_self(
    data: UserUpdate,
    token: str = Depends(oauth2_scheme),
    auth_service: AuthController = Depends(get_auth_controller),
):
    try:
        await check_role(UserRole.MEMBER.value, token)
        user = await auth_service.get_current_user(token)
        
        updated_user = await update_user(user.id, data)
        return UserDisplay.model_validate(updated_user)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
