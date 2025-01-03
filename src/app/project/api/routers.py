from fastapi import APIRouter

from .create import router as create_project_api
from .find import router as find_project_api
from .delete import router as delete_project_api
from .update import router as update_project_api
from .set_active import router as set_active

project_router = APIRouter()

project_router.include_router(create_project_api)
project_router.include_router(find_project_api)
project_router.include_router(delete_project_api)
project_router.include_router(update_project_api)
project_router.include_router(set_active)
