from tortoise.exceptions import DoesNotExist
from datetime import datetime

from src.config.log import logger
from src.app.user.model import UserModel
from src.app.link.model import LinkModel
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.exceptions.entities import NotFoundError
from src.base.controller import BaseController
from src.app.project.model import ProjectModel
from src.app.chat.model import ChatModel


class LinkController(BaseController[LinkModel]):
    async def get_by_url(self, url: str) -> LinkModel:
        try:
            return await LinkModel.get(link_url=url).prefetch_related(
                "project", "chat"
            )
        except DoesNotExist:
            raise NotFoundError()

    async def permission_for_create_link(self, project_id, chat_id, current_user):
        if project_id:
            project = await ProjectModel.get(id=project_id)
            if not project:
                raise NotFoundError()

            project_owner = await project.owner
            if current_user != project_owner:
                raise NotFoundError()
        else:
            chat = await ChatModel.get(id=chat_id)
            if not chat:
                raise NotFoundError()
            related_project = await chat.project
            owner = await related_project.owner
            if current_user != owner:
                raise NotFoundError()

    @staticmethod
    async def log_link_usage(link: str, user: UserModel, ip_address: str):
        log_message = (
            f"[{datetime.now()}] Link Accessed: {link.link_url} | "
            f"Resource Type: {'Project' if link.project else 'Chat'} | "
            f"Accessed By: {user} | IP: {ip_address} | Expired: {link.is_expired}"
        )
        logger.info(log_message)


def get_link_controller() -> BaseController:
    return LinkController(LinkModel)
