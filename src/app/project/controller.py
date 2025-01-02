from typing import List
from tortoise.exceptions import DoesNotExist

from src.helpers.exceptions.entities import NotFoundError
from src.base.controller import BaseController
from src.app.project.model import ProjectModel
from src.app.user.model import UserModel


class ProjectController(BaseController[ProjectModel]):
    async def get_projects_by_user(self, user: UserModel) -> List[ProjectModel]:
        return await self.model.filter(owner=user).all()

    async def get_project_owner(id: int) -> UserModel:
        try:
            project = await ProjectModel.get(id=id).prefetch_related("owner")
            return project.owner
        except DoesNotExist:
            raise NotFoundError()


def get_project_controller() -> BaseController:
    return ProjectController(ProjectModel)
