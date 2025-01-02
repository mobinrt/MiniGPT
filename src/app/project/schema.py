from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=15)
    description: Optional[str] = Field(max_length=100, default=None)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ProjectDisplay(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
