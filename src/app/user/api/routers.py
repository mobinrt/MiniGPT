from fastapi import APIRouter

from .user_apis import router as crud_user_api
user_router = APIRouter()

user_router.include_router(crud_user_api)