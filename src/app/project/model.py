from tortoise import fields

from src.base.model import BaseModel
from src.app.chat.model import ChatModel  # noqa: F401


class ProjectModel(BaseModel):
    owner = fields.ForeignKeyField(
        "models.UserModel", related_name="projects", on_delete=fields.CASCADE
    )

    name = fields.CharField(max_length=15)
    description = fields.CharField(max_length=100, null=True)
    
    chats = fields.ReverseRelation["ChatModel"]

    class Meta:
        table = "projects"
