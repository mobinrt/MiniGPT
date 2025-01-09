from fastapi import APIRouter

prompt_router = APIRouter(
    prefix="/prompt",
    tags=["prompt"],
)

responce_router = APIRouter(
    prefix="/responce",
    tags=["responce"],
)
