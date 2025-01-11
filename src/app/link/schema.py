from pydantic import BaseModel, Field, field_validator
from typing import Optional


class LinkCreate(BaseModel):
    project_id: Optional[int] = Field(default=None)
    chat_id: Optional[int] = Field(default=None)
    is_public: bool = Field(default=False)

    @field_validator("project_id", "chat_id", mode="before")
    def check_one_of_both(cls, v, values, field):
        if field.name == "project_id":
            if v is None and values.get("chat_id") is None:
                raise ValueError("Either project_id or chat_id must be provided.")
        elif field.name == "chat_id":
            if v is None and values.get("project_id") is None:
                raise ValueError("Either project_id or chat_id must be provided.")

        if values.get("project_id") is not None and values.get("chat_id") is not None:
            raise ValueError("Only one of project_id or chat_id must be provided.")

        return v
