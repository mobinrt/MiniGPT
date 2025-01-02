from functools import wraps
from fastapi import HTTPException, status

from src.helpers.auth.controller import AuthController
from src.helpers.exceptions.auth_exceptions import AccessDenied


def role_required(required_role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs.get("token")
            if not token:
                raise AccessDenied()

            auth_service = AuthController()

            try:
                user_role = await auth_service.get_role_from_token(token)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.message
                )

            if user_role != required_role:
                raise AccessDenied()

            return await func(*args, **kwargs)

        return wrapper

    return decorator


async def check_role(role: str, token: str):
    auth_service = AuthController()
    user_role = await auth_service.get_role_from_token(token)
    if user_role != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You do not have the required role",
        )
