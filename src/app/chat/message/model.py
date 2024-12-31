from tortoise import fields


from src.helpers.enum.message_status import MessageStatus
from src.helpers.enum.responce_status import ResponceStatus
from src.base.model import BaseModel


class MessageModel(BaseModel):
    chat = fields.ForeignKeyField("models.ChatModel", on_delete=fields.CASCADE)

    content = fields.TextField()
    status = fields.CharEnumField(
        enum_type=MessageStatus, default=MessageStatus.SENT.value
    )

    class Meta:
        abstract = True


class PromptModel(MessageModel):
    class Meta:
        table = "prompts"
        indexes = [("chat",)]


class ResponceModel(MessageModel):
    prompt = fields.ForeignKeyField(
        "models.PromptModel", related_name="responces", on_delete=fields.CASCADE
    )
    like_status = fields.CharEnumField(
        enum_type=ResponceStatus, default=ResponceStatus.NONE.value
    )

    class Meta:
        table = "responces"
        indexes = [("prompt",)]
