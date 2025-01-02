from fastapi import HTTPException, status, Depends
from . import router

from src.app.user.model import UserModel
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.auth.rbac import role_required
from src.helpers.enum.user_role import UserRole
from src.helpers.auth.controller import oauth2_scheme
from src.helpers.auth.dependencies import get_current_user
from src.app.project.controller import ProjectController, get_project_controller
from src.helpers.exceptions.entities import NotFoundError


@router.delete(
    "/me/{id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def delete_project_me(
    id: int,
    current_user: UserModel = Depends(get_current_user),
    controller: ProjectController = Depends(get_project_controller),
):
    try:
        project = await controller.get_by_id(id)
        if not current_user.__eq__(project.owner):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can not delete this project.",
            )
        await controller.delete(id)
        return {"message": "Your project has been deleted successfully"}
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
@role_required(UserRole.ADMIN.value)
async def delete_project_by_admin(
    id: int,
    token: str = Depends(oauth2_scheme),
    controller: ProjectController = Depends(get_project_controller),
):
    try:
        await controller.delete(id)
        return {"message": "Project deleted successfully by admin"}
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
