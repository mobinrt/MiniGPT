from tortoise.exceptions import DoesNotExist
from typing import Sequence

from src.app.user.model import UserModel
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.hash import get_password_hash
from src.helpers.exceptions.user import DeleteAdmin


async def create_user(username: str, email: str, password: str) -> UserModel:
    if not username:
        raise BaseError("Username should not be blank!")

    if not email:
        raise BaseError("Email should not be blank!")

    existing_user = await UserModel.filter(email=email).first()
    if existing_user:
        raise BaseError("Email is already in use")

    return await UserModel.create_user(
        username=username, email=email, password=password
    )


async def get_user_by_email(email: str) -> UserModel:
    try:
        return await UserModel.get(email=email)
    except DoesNotExist:
        raise BaseError("User not found")


async def get_user_by_id(user_id: int) -> UserModel:
    try:
        return await UserModel.get(id=user_id)
    except DoesNotExist:
        raise BaseError("User not found")


async def get_users() -> Sequence[UserModel]:
    try:
        return await UserModel.all()
    except DoesNotExist:
        raise BaseError("Not found any user")


async def update_user(user_id: int, data: dict) -> UserModel:
    user = await get_user_by_id(user_id)
    for field, value in data.items():
        if field == "password":
            value = get_password_hash(value)
        setattr(user, field, value)
    await user.save()
    return user


async def delete_user(user_id: int):
    user = await get_user_by_id(user_id)
    if user.is_admin:
        raise DeleteAdmin()
    await user.delete()
