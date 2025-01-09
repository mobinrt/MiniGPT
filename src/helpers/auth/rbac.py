from functools import wraps
from fastapi import HTTPException, status, Depends

from src.helpers.auth import oauth2_scheme
from src.helpers.auth.controller import AuthController
from src.helpers.exceptions.auth_exceptions import AccessDenied
from src.app.user.model import UserModel


def role_required(required_role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs.get("token")
            if not token:
                raise AccessDenied()

            user_role = await get_role(token)
            if user_role != required_role:
                raise AccessDenied()

            return await func(*args, **kwargs)

        return wrapper

    return decorator


async def validate_role(token: str, required_role: str):
    user_role = await get_role(token)
    if user_role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User role must be {required_role} to perform this action",
        )


async def get_role(token: str):
    auth_service = AuthController()
    try:
        return await auth_service.get_role_from_token(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
