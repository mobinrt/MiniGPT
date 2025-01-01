from tortoise import fields

from src.base.model import BaseModel
from src.app.chat.message.model import MessageModel  # noqa: F401


class ChatModel(BaseModel):
    project = fields.ForeignKeyField(
        "models.ProjectModel", related_name="chats", on_delete=fields.CASCADE
    )

    title = fields.CharField(max_length=50)
    is_active = fields.BooleanField(default=False)

    messages = fields.ReverseRelation["MessageModel"]

    class Meta:
        table = "chats"
        indexes = [("project",)]
        
    async def set_active(self):
        self.is_active = True
        
    async def set_deactive(self):
        self.is_active = False
    
