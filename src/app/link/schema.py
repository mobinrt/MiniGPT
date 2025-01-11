from pydantic import BaseModel, Field, model_validator
from typing import Optional


class LinkCreate(BaseModel):
    project_id: Optional[int] = Field(default=None)
    chat_id: Optional[int] = Field(default=None)
    is_public: bool = Field(default=False)

    @model_validator(mode="after")
    def check_one_of_both(cls, values):
        project_id = values.project_id
        chat_id = values.chat_id

        if project_id is None and chat_id is None:
            raise ValueError("Either project_id or chat_id must be provided.")

        if project_id is not None and chat_id is not None:
            raise ValueError("Only one of project_id or chat_id must be provided.")

        return values
