from fastapi import APIRouter

from .create import router as create_user_api
from .find import router as find_user_api
from .delete import router as delete_user_api
from .update import router as update_user_api
user_router = APIRouter()

user_router.include_router(create_user_api)
user_router.include_router(find_user_api)
user_router.include_router(delete_user_api)
user_router.include_router(update_user_api)