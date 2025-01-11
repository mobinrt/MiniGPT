from fastapi import APIRouter

from .prompt_apis import router as prompt_api
from .chat_apis import router as chat_api

# from .find import router as find_chat_api
# from .delete import router as delete_chat_api
# from .update import router as update_chat_api

chat_router = APIRouter()

chat_router.include_router(chat_api)
# chat_router.include_router(find_chat_api)
# chat_router.include_router(delete_chat_api)
# chat_router.include_router(update_chat_api)


prompt_router = APIRouter()

prompt_router.include_router(prompt_api)