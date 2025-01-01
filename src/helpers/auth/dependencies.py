from fastapi import Depends

from .controller import AuthController
from .auth_usecase import AuthUseCase


async def get_auth_controller() -> AuthController:
    return AuthController()


async def get_auth_usecase(
    auth_controller: AuthController = Depends(get_auth_controller),
) -> AuthUseCase:
    return AuthUseCase(auth_controller)
