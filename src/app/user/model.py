from tortoise import fields
from tortoise.validators import RegexValidator
import re   

from src.base.model import BaseModel


class UserModel(BaseModel):
    username = fields.CharField(max_length=50)
    email = fields.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                flags=re.IGNORECASE,
            )
        ],
        error_messages={"invalid": "Your email is invalid."},
    )

    password_hash = fields.CharField(max_length=200)
    is_admin = fields.BooleanField(default=False)
    is_premium = fields.BooleanField(default=False)
    pic_url = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "users"
        indexes = [("email",)]
