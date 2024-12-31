from functools import wraps
from fastapi import HTTPException, status

from src.app.features.user.auth.service.auth_service_imp import AuthServiceImp
from src.app.core.exception.auth_exceptions import AccessDenied

def role_required(required_role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            token = kwargs.get('token')
            if not token:
                raise AccessDenied('Not authenticated')

            auth_service = AuthServiceImp()
            
            try:
                user_role = await auth_service.get_role_from_token(token)
            except Exception as e:
                raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.message
            )

            if user_role != required_role:
                raise AccessDenied('Access forbidden: insufficient role')

            return await func(*args, **kwargs)

        return wrapper
    return decorator
