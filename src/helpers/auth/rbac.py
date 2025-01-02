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
