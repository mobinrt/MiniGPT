from fastapi import Depends

from .controller import AuthController, oauth2_scheme
from .auth_usecase import AuthUseCase


async def get_auth_controller() -> AuthController:
    return AuthController()


async def get_auth_usecase(
    auth_controller: AuthController = Depends(get_auth_controller),
) -> AuthUseCase:
    return AuthUseCase(auth_controller)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_controller: AuthController = Depends(get_auth_controller),
):
    return await auth_controller.get_current_user(token)
