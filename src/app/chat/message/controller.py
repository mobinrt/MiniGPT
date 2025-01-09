from typing import List
from tortoise.exceptions import DoesNotExist

from src.helpers.exceptions.entities import NotFoundError
from src.base.controller import BaseController
from src.app.chat.message.model import PromptModel, ResponceModel
from src.app.user.model import UserModel


class PromptController(BaseController[PromptModel]):
    async def permission_to_access_prompt(self, prompt_id: int, current_user: UserModel) -> PromptModel:
        prompt = await self.get_by_id(prompt_id)   
        related_chat = await prompt.chat
        related_project = await related_chat.project
        project_owner = await related_project.owner

        if current_user != project_owner and not current_user.is_admin:
            raise NotFoundError()
        return prompt


def get_prompt_controller() -> BaseController:
    return PromptController(PromptModel)


class ResponceController(BaseController[ResponceModel]):
    pass


def get_responce_controller() -> BaseController:
    return ResponceController(ResponceModel)
