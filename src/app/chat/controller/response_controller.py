from tortoise.exceptions import DoesNotExist

from src.helpers.exceptions.entities import NotFoundError
from src.base.controller import BaseController
from src.app.chat.model.message_model import ResponceModel


class ResponceController(BaseController[ResponceModel]):
    pass


def get_responce_controller() -> BaseController:
    return ResponceController(ResponceModel)
