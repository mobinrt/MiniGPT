# from typing import List
# from tortoise.exceptions import DoesNotExist
from tortoise.exceptions import DoesNotExist

# from src.helpers.exceptions.entities import NotFoundError
from src.base.controller import BaseController
from src.app.project.model import ProjectModel
from src.app.chat.model import ChatModel
from src.helpers.exceptions.entities import NotFoundError


class ChatController(BaseController[ChatModel]):
    async def get_project_by_id(self, id: int) -> ProjectModel:
        try:
            return await ProjectModel.get_or_none(id=id)    
        except DoesNotExist:
            raise NotFoundError()



def get_chat_controller() -> BaseController:
    return ChatController(ChatModel)
