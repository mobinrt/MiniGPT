from fastapi import HTTPException, status, Depends
from . import router

from src.app.project.schema import ProjectDisplay, ProjectUpdate
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.auth.dependencies import get_current_user
from src.app.user.model import UserModel
from src.app.project.controller import ProjectController, get_project_controller
from src.helpers.exceptions.entities import NotFoundError


@router.put(
    "/update/{id}",
    response_model=ProjectDisplay,
    status_code=status.HTTP_200_OK,
)
async def update_project(
    id: int,
    data: ProjectUpdate,
    controller: ProjectController = Depends(get_project_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        project = await controller.get_by_id(id)
        
        if not current_user.__eq__(project.owner):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized to access this project",
            )

        dict_data = data.model_dump()
        updated_project = await controller.update(id, dict_data)
        return ProjectDisplay.model_validate(updated_project)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    # except Exception as _e:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
