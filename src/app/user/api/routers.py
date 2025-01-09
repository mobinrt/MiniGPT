from fastapi import APIRouter

from .crud import router as crud_user_api
user_router = APIRouter()

user_router.include_router(crud_user_api)