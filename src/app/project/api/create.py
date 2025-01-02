from fastapi import HTTPException, status, Depends
from . import router

from src.app.project.schema import ProjectCreate, ProjectDisplay
from src.app.project.controller import ProjectController, get_project_controller
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.auth import oauth2_scheme
from src.helpers.auth.dependencies import get_current_user
from src.app.user.model import UserModel


@router.post(
    "/create",
    response_model=ProjectDisplay,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"}},
)
async def create_project(
    data: ProjectCreate,
    token: str = Depends(oauth2_scheme),
    controller: ProjectController = Depends(get_project_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        project = await controller.create(owner=current_user, **data.model_dump())
        return ProjectDisplay(
        id=project.id,
        name=project.name,
        description=project.description,
        owner_id=project.owner.id,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    # except Exception as _e:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
