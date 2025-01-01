from fastapi import APIRouter

from .create import router as create_user_api

user_router = APIRouter()

user_router.include_router(create_user_api)
