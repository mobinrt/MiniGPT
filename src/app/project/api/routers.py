from fastapi import APIRouter

from .project_apis import router as crud_project_api

project_router = APIRouter()

project_router.include_router(crud_project_api)