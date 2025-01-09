from pydantic import BaseModel, Field
from datetime import datetime

# from src.helpers.enum.message_status import MessageStatus
# from src.helpers.enum.responce_status import ResponceStatus


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1)


class PromptCreate(MessageBase):
    chat_id: int


class ResponceCreate(MessageBase):
    prompt_id: int


class PromptUpdate(MessageBase):
    pass


class MessageDisplay(BaseModel):
    id: int
    chat_id: int
    content: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PromptDisplay(MessageDisplay):
    pass


class ResponceDisplay(MessageDisplay):
    prompt_id: int
    like_status: str
