from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.pydantic import pydantic_queryset_creator

from src.app.user.model import UserModel


UserIn_Pydantic = pydantic_model_creator(
    UserModel, name="UserIn", exclude_readonly=True
)

UserList_Pydantic = pydantic_queryset_creator(UserModel)

User_Pydantic = pydantic_model_creator(
    UserModel, name="UserModel", include=("projects",)
)
