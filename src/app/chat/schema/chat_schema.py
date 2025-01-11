from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ChatCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=15)
    project_id: int

class ChatUpdate(BaseModel):
    title: Optional[str] = Field(max_length=15, default=None)


class ChatDisplay(BaseModel):
    id: int
    project_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
