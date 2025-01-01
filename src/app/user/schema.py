from tortoise.contrib.pydantic import pydantic_model_creator  # noqa: F401
from tortoise.contrib.pydantic import pydantic_queryset_creator  # noqa: F401
from pydantic import BaseModel, Field, model_validator, EmailStr, HttpUrl
from typing import Optional

from src.app.user.model import UserModel  # noqa: F401


class UserCreate(BaseModel):
    username: str = Field(..., pattern=r"^[a-z]+$", min_length=1, max_length=15)
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    confirm_password: str

    @model_validator(mode="before")
    def check_passwords_match(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")
        if password != confirm_password:
            raise ValueError("Passwords do not match!!")
        return values


class UserDisplay(BaseModel):
    username: str
    email: EmailStr
    is_premium: bool
    image_url: Optional[HttpUrl] = None

    model_config = {"from_attributes": True}


class UserUpdate(UserCreate):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None


# UserDisplay = pydantic_model_creator(
#     UserModel, name="UserCreate", exclude=["password_hash"]
# )


# UserList = pydantic_queryset_creator(UserModel, exclude=["password_hash"])

# UserDisplayProejcts = pydantic_model_creator(
#     UserModel, name="User", include=("projects",)
# )
