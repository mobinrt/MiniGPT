from fastapi import APIRouter

from .link_apis import router as crud_link_api

link_router = APIRouter()

link_router.include_router(crud_link_api)