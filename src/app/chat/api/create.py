# from fastapi import HTTPException, status, Depends
# from . import router
# from redis.exceptions import RedisError


# from src.app.chat.schema import ChatCreate, ChatDisplay
# from src.app.chat.controller import get_chat_controller, ChatController
# from src.helpers.exceptions.base_exception import BaseError
# from src.helpers.exceptions.entities import NotFoundError
# from src.app.project.model import ProjectModel
# from src.helpers.auth.controller import oauth2_scheme
# from src.app.project.dependencies import get_active_project


# @router.post(
#     "/create",
#     response_model=ChatDisplay,
#     status_code=status.HTTP_201_CREATED,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"},
#         status.HTTP_404_NOT_FOUND: {"description": "Project not found"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# async def create_chat(
#     chat_data: ChatCreate,
#     active_project: ProjectModel = Depends(get_active_project),
#     controller: ChatController = Depends(get_chat_controller),
#     token: str = Depends(oauth2_scheme),
# ):
#     try:
#         if active_project is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
#             )
#         new_chat = await controller.create(
#             project=active_project, is_active=False, **chat_data.model_dump()
#         )

#         return ChatDisplay(
#             id=new_chat.id,
#             project_id=new_chat.project_id,
#             is_active=new_chat.is_active,
#             created_at=new_chat.created_at,
#             updated_at=new_chat.updated_at,
#         )
#     except NotFoundError as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)

#     except BaseError as ex:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)

#     except RedisError as redis_error:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Redis error: {str(redis_error)}",
#         )

#     # except Exception as _e:
#     #     # logger.error(f"Unexpected error: {str(_e)}")
#     #     raise HTTPException(
#     #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#     #         detail="An unexpected error occurred. Please try again later.",
#     #     )
