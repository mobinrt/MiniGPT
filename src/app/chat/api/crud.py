from fastapi import HTTPException, status, Depends
from . import router


from src.app.chat.schema import ChatCreate, ChatDisplay
from src.app.chat.controller import get_chat_controller, ChatController
from src.app.user.model import UserModel
from src.app.project.model import ProjectModel

from src.helpers.auth.dependencies import get_current_user
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.exceptions.entities import NotFoundError
from src.helpers.auth.controller import oauth2_scheme


@router.post(
    "/create",
    response_model=ChatDisplay,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"},
        status.HTTP_404_NOT_FOUND: {"description": "Project not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def create_chat(
    chat_data: ChatCreate,
    controller: ChatController = Depends(get_chat_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        active_project = await controller.get_project_by_id(chat_data.project_id)
        project_owner = await active_project.owner

        if current_user != project_owner:
            raise BaseError("Project not found")

        new_chat = await controller.create(
            project=active_project, is_active=False, **chat_data.model_dump()
        )

        return ChatDisplay.model_validate(new_chat)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)

    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)

    # except Exception as _e:
    #     # logger.error(f"Unexpected error: {str(_e)}")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="An unexpected error occurred. Please try again later.",
    #     )
