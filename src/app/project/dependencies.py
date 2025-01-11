# from fastapi import Depends
# from redis.asyncio import Redis
# from tortoise.exceptions import DoesNotExist

# from src.helpers.auth.dependencies import get_current_user
# from src.app.user.model import UserModel
# from src.helpers.exceptions.base_exception import BaseError
# from src.helpers.exceptions.entities import NotFoundError
# from src.config.redis import get_redis_client
# from .controller import ProjectController, get_project_controller


# async def get_active_project(
#     current_user: UserModel = Depends(get_current_user),
#     redis_client: Redis = Depends(get_redis_client),
#     controller: ProjectController = Depends(get_project_controller),
# ):
#     active_project_id = await redis_client.get(f"active_project:{current_user.id}")

#     if not active_project_id:
#         raise BaseError("No active project set")

#     try:
#         project = await controller.get_by_id(id=int(active_project_id))
#     except DoesNotExist as e:
        
#         raise NotFoundError()

#     return project
