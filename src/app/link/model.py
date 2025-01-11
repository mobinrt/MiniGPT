from tortoise import fields
from datetime import datetime, timedelta
import uuid

from src.base.model import BaseModel


class LinkModel(BaseModel):
    project = fields.ForeignKeyField(
        "models.ProjectModel", related_name="links", on_delete=fields.CASCADE, null=True
    )
    chat = fields.ForeignKeyField(
        "models.ChatModel", related_name="links", on_delete=fields.CASCADE, null=True
    )
    user = fields.ForeignKeyField(
        "models.UserModel", related_name="links", on_delete=fields.CASCADE
    )

    link_url = fields.CharField(max_length=255, null=True)
    is_public = fields.BooleanField(default=False)

    class Meta:
        table = "links"
        indexes = [("user", "project", "chat", "link_url")]

    @property
    def expired_at(self) -> datetime:
        if not self.created_at:
            raise ValueError("The 'created_at' field is not set.")
        return self.created_at + timedelta(hours=24)

    @property
    def is_expired(self) -> bool:
        expired_at_naive = self.expired_at.replace(tzinfo=None) 
        return datetime.now() > expired_at_naive

    def generate_link_url(self, base_url: str) -> None:
        unique_id = uuid.uuid4().hex
        self.link_url = f"{base_url}/{unique_id}"

    async def set_public(self):
        self.is_public = True

    async def set_private(self):
        self.is_public = True




