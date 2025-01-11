from pydantic import BaseModel, Field
from datetime import datetime


class MessageBase(BaseModel):
    content: str = Field(..., min_length=1)


class MessageDisplay(BaseModel):
    id: int
    chat_id: int
    content: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
