from fastapi import APIRouter

from .prompt_apis import router as prompt_api
from .chat_apis import router as chat_api

chat_router = APIRouter()

chat_router.include_router(chat_api)

prompt_router = APIRouter()

prompt_router.include_router(prompt_api)
