from tortoise import fields
from tortoise.validators import RegexValidator
import re

from src.base.model import BaseModel
from src.app.project.model import ProjectModel  # noqa: F401
from src.helpers.hash import get_password_hash
from src.helpers.exceptions.base_exception import BaseError

class UserModel(BaseModel):
    username = fields.CharField(max_length=50)
    email = fields.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                flags=re.IGNORECASE,
            )
        ],
        error_messages={'invalid': 'Your email is invalid.'},
    )

    password_hash = fields.CharField(max_length=200)
    is_admin = fields.BooleanField(default=False)
    is_premium = fields.BooleanField(default=False)
    pic_url = fields.CharField(max_length=255, null=True)

    projects = fields.ReverseRelation['ProjectModel']

    class Meta:
        table = 'users'
        indexes = [('email',)]

    class PydanticMeta:
        include = ('projects',)
        exclude = ['is_admin', 'password_hash'] 
        max_recursion = 2

    async def upgrade_premium(self):
        self.is_premium = True
        await self.save()

    async def downgrade_premium(self):
        self.is_premium = True
        await self.save()

    @classmethod
    async def create_user(cls, username: str, email: str, password: str) -> 'UserModel':
        email = email.lower().strip()
        hashed_password = cls._hash_password(password)
        try:
            return await cls.create(
                username=username, email=email, password_hash=hashed_password
            )
        except BaseError as e:
            raise BaseError(f'Failed to create user: {str(e)}')

    @staticmethod
    def _hash_password(password: str) -> str:
        return get_password_hash(password)
