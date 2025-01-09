from fastapi import APIRouter

from .crud import prompt_router as crud_prompt_api

message_router = APIRouter()

message_router.include_router(crud_prompt_api)