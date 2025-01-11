# from typing import List
# from tortoise.exceptions import DoesNotExist
from tortoise.exceptions import DoesNotExist

# from src.helpers.exceptions.entities import NotFoundError
from src.base.controller import BaseController
from src.app.project.model import ProjectModel
from src.app.user.model import UserModel
from src.app.chat.model import ChatModel
from src.helpers.exceptions.entities import NotFoundError


class ChatController(BaseController[ChatModel]):
    async def get_project_by_id(self, id: int) -> ProjectModel:
        try:
            return await ProjectModel.get(id=id)    
        except DoesNotExist:
            raise NotFoundError()

    async def permission_to_access_chat(self, chat_id: int, current_user: UserModel) -> ChatModel:
        chat = await self.get_by_id(chat_id)   
        related_project = await chat.project
        project_owner = await related_project.owner
        
        if current_user != project_owner and not current_user.is_admin:
            raise NotFoundError()
        return chat


def get_chat_controller() -> BaseController:
    return ChatController(ChatModel)
