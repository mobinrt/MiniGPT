# from fastapi import HTTPException, status, Depends
# from tortoise.exceptions import DoesNotExist
# from redis.asyncio import Redis
# from typing import Dict

# from . import router
# from src.app.user.model import UserModel
# from src.helpers.auth.dependencies import get_current_user
# from src.app.project.controller import get_project_controller, ProjectController
# from src.helpers.exceptions.base_exception import BaseError
# from src.config.redis import get_redis_client
# @router.post(
#     "/{project_id}/set-active",
#     response_model=Dict,
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_403_FORBIDDEN: {"description": "Not authorized"},
#         status.HTTP_404_NOT_FOUND: {"description": "Project not found"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Server error"},
#     },
# )
# async def set_active_project(
#     project_id: int,
#     current_user: UserModel = Depends(get_current_user),
#     redis_client: Redis = Depends(get_redis_client),
#     controller: ProjectController = Depends(get_project_controller),
# ):
#     try:
#         project = await controller.get_by_id(project_id)

#         if not current_user.__eq__(project.owner):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Not authorized to set this project as active",
#             )

#         current_user.active_project_id = project.id
#         await redis_client.set(f"active_project:{current_user.id}", project_id)
#         return {"detail": "Active project set successfully"}
#     except DoesNotExist:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Project not found",
#         )

#     except BaseError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Validation error: {str(e)}",
#         )

#     except Exception as _e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An unexpected error occurred",
#         )
