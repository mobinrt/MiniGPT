# from typing import List
# from tortoise.exceptions import DoesNotExist

# from src.helpers.exceptions.entities import NotFoundError
from src.base.controller import BaseController
# from src.app.project.model import ProjectModel
from src.app.chat.model import ChatModel


class ChatController(BaseController[ChatModel]):
    pass


def get_chat_controller() -> BaseController:
    return ChatController(ChatModel)
