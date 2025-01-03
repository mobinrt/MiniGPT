from fastapi import HTTPException, status, Depends
from . import router

from src.helpers.auth.controller import AuthController
from src.app.user.model import UserModel
from src.helpers.auth.dependencies import get_current_user, get_auth_controller
from src.app.project.controller import get_project_controller, ProjectController
from src.helpers.enum.user_role import UserRole


@router.post(
    "/{project_id}/set-active",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_403_FORBIDDEN: {"description": "Not authorized"}},
)
async def set_active_project(
    project_id: int,
    current_user: UserModel = Depends(get_current_user),
    auth_controller: AuthController = Depends(get_auth_controller),
    controller: ProjectController = Depends(get_project_controller),
):
    project = await controller.get_by_id(project_id)
    if not current_user.__eq__(project.owner):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to set this project as active",
        )

    current_user.active_project_id = project.id

    token = auth_controller.create_access_token(current_user.id, UserRole.MEMBER)
    return {"detail": "Active project updated", "access_token": token}
