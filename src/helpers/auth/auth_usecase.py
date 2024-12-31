from src.app.features.user.auth.service.auth_service_imp import AuthServiceImp
from src.app.core.exception.auth_exceptions import InvalidCredentialsError
from src.app.features.user.auth.domain.auth_schemas import TokenDisplay, AccessTokenDisplay
from src.app.features.user.domain.user_schema import UserDisplay
from src.app.core.utility.hash import verify_password
from src.app.core.enum.user_role import UserRole

from tortoise.exceptions import ValidationError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

class AuthUseCase:
    def __init__(self, auth_service: AuthServiceImp):
        self.auth_service = auth_service

    async def get_token(self, request: OAuth2PasswordRequestForm) -> TokenDisplay:
        email = request.username
        try:
            user = await self.auth_service.get_user_by_email(email)
        except ValidationError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid email format.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
        
        if not user or not verify_password(request.password, user.password_hash):
            raise InvalidCredentialsError

        role = UserRole.ADMIN if user.is_admin else UserRole.MEMBER
        access_token = await self.auth_service.create_access_token(user.id, role)
        refresh_token = await self.auth_service.create_refresh_token(user.id)

        return TokenDisplay(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='bearer'
        )

    async def get_current_user(self, token: str):
        user = await self.auth_service.get_current_user(token)
        print(user)
        return UserDisplay.model_validate(user)

    async def refresh_access_token(self, token: str) -> AccessTokenDisplay:
        role = await self.auth_service.get_role_from_token(token)
        new_access_token = await self.auth_service.create_access_token(token, role)
        return AccessTokenDisplay(
            access_token=new_access_token, 
            token_type='bearer'
            )
 