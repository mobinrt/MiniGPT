from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProjectCreate(BaseModel):
    name: Optional[str] = Field(max_length=15, default=None)
    description: Optional[str] = Field(max_length=100, default=None)


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(max_length=15, default=None)
    description: Optional[str] = Field(max_length=100, default=None)


class ProjectDisplay(BaseModel):
    id: int
    owner_id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
