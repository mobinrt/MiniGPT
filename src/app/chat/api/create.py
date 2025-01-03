from fastapi import HTTPException, status, Depends
from . import router

from src.app.chat.schema import ChatCreate, ChatDisplay
from src.app.chat.controller import get_chat_controller, ChatController
from src.helpers.exceptions.base_exception import BaseError
from src.app.project.model import ProjectModel
from src.middleware.dependencies import get_active_project_id
from src.helpers.auth.controller import oauth2_scheme


@router.post(
    "/create",
    response_model=ChatDisplay,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden access"},
        status.HTTP_404_NOT_FOUND: {"description": "Project not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def create_chat(
    chat_data: ChatCreate,
    active_project_id: int = Depends(get_active_project_id),
    controller: ChatController = Depends(get_chat_controller),
    token: str = Depends(oauth2_scheme),
):
    try:
        if not active_project_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Active project not found"
            )
        project = await ProjectModel.get_or_none(id=active_project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )
        new_chat = await controller.create(project=project, **chat_data.model_dump())
        return ChatDisplay.model_validate(new_chat)

    except BaseError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as _e:
        # logger.error(f"Unexpected error: {str(_e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )
