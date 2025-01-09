from fastapi import APIRouter

from .crud import router as crud_project_api

project_router = APIRouter()

project_router.include_router(crud_project_api)