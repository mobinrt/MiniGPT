from tortoise.exceptions import DoesNotExist
import logging
from datetime import datetime

from src.app.user.model import UserModel
from src.app.link.model import LinkModel
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.exceptions.entities import NotFoundError
from src.base.controller import BaseController


class LinkController(BaseController[LinkModel]):
    async def get_by_url(self, unique_id: str) -> LinkModel:
        try:
            return await LinkModel.get(link_url=unique_id).prefetch_related(
                "project", "chat"
            )
        except DoesNotExist:
            raise NotFoundError()

    @staticmethod
    async def log_link_usage(link: str, user: UserModel, ip_address: str):
        log_message = (
            f"[{datetime.now()}] Link Accessed: {link.link_url} | "
            f"Resource Type: {'Project' if link.project else 'Chat'} | "
            f"Accessed By: {user} | IP: {ip_address} | Expired: {link.is_expired}"
        )
        logging.info(log_message)


def get_link_controller() -> BaseController:
    return LinkController(LinkModel)
