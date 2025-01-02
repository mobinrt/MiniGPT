from fastapi import HTTPException, status, Depends
from typing import List

from . import router
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.auth.rbac import role_required
from src.helpers.enum.user_role import UserRole
from src.helpers.auth import oauth2_scheme
from src.app.project.schema import ProjectDisplay
from src.app.project.controller import ProjectController, get_project_controller
from src.helpers.auth.dependencies import get_current_user
from src.app.user.model import UserModel


@router.get(
    "/",
    response_model=List[ProjectDisplay],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found any project"}},
)
@role_required(UserRole.ADMIN.value)
async def find_projects(
    token: str = Depends(oauth2_scheme),
    controller: ProjectController = Depends(get_project_controller),
):
    try:
        projects = await controller.get_entities()
        project_data = [ProjectDisplay.model_validate(project) for project in projects]
        return project_data
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/me",
    response_model=List[ProjectDisplay],
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found any project"}},
)
async def find_projects_me(
    controller: ProjectController = Depends(get_project_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        projects = await controller.get_projects_by_user(current_user)
        project_data = [ProjectDisplay.model_validate(project) for project in projects]
        return project_data
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/{id}",
    response_model=ProjectDisplay,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Project not found"}},
)
@role_required(UserRole.ADMIN.value)
async def find_project_by_id(
    id: int,
    token: str = Depends(oauth2_scheme),
    controller: ProjectController = Depends(get_project_controller),
):
    try:
        project = await controller.get_by_id(id)
        return ProjectDisplay.model_validate(project)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
