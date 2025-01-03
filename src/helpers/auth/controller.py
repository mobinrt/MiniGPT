from datetime import timedelta, datetime
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status

from src.app.user.model import UserModel
from src.config import settings
from src.helpers.enum.user_role import UserRole
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.exceptions.auth_exceptions import InvalidTokenError
from src.helpers.exceptions.entities import NotFoundError
from . import oauth2_scheme


class AuthController:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS

    async def get_user_by_email(self, email: str) -> UserModel | None:
        return await UserModel.get_or_none(email=email)

    async def get_user_by_id(self, id: int) -> UserModel | None:
        return await UserModel.get_or_none(id=id)

    async def create_access_token(self, user_id: int, role: UserRole) -> str:
        expires_delta = timedelta(minutes=self.access_token_expire_minutes)
        user = await self.get_user_by_id(user_id)
        data = {
            "sub": str(user_id),
            "role": role.value,
            "active_project_id": user.active_project_id
            if user.active_project_id
            else None,
            "exp": datetime.now() + expires_delta,
        }
        to_encode = data.copy()
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def create_refresh_token(self, user_id: int) -> str:
        expires_delta = timedelta(days=self.refresh_token_expire_days)
        to_encode = {"sub": str(user_id), "exp": datetime.now() + expires_delta}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def get_current_user(self, token: str = Depends(oauth2_scheme)) -> UserModel:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise InvalidTokenError()
        except JWTError:
            raise InvalidTokenError()

        user = await UserModel.get_or_none(id=user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def get_role_from_token(
        self, token: str = Depends(oauth2_scheme)
    ) -> UserRole:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            role = payload.get("role")
            if not role:
                raise BaseError("Role not found in token")
            return UserRole(role)
        except JWTError:
            raise InvalidTokenError()

    async def get_user_id_by_token(self, token) -> UserModel:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                raise InvalidTokenError()
            return user_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired."
            )
        except jwt.JWTError:
            raise InvalidTokenError()
