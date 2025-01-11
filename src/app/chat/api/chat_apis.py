from fastapi import HTTPException, status, Depends, Request, Query, APIRouter

from src.app.chat.schema.chat_schema import ChatCreate, ChatUpdate
from src.app.chat.controller import get_chat_controller, ChatController
from src.app.user.model import UserModel
from src.app.chat.model import ChatModel

from src.helpers.auth.dependencies import get_current_user
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.exceptions.entities import NotFoundError
from src.helpers.schema import ChatResponseScheme
from src.helpers.filter import Filter
from src.helpers.pagination import Paginator, paginate_decorator
from src.helpers.order_by import OrderBy
from src.helpers.select import Select
from src.helpers.filter_schema import create_filter_schema

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


ChatFilterSchema = create_filter_schema(
    ChatModel,
    excludes=["created_at", "updated_at", "links_id", "sessions_id"],
    filter_operations=["contains", "exact"],
)


@router.post(
    "/",
    response_model=ChatResponseScheme,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"},
        status.HTTP_404_NOT_FOUND: {"description": "Project not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def create(
    chat_data: ChatCreate,
    controller: ChatController = Depends(get_chat_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        active_project = await controller.get_project_by_id(chat_data.project_id)
        project_owner = await active_project.owner

        if current_user != project_owner:
            raise NotFoundError()

        new_chat = await controller.create(
            project=active_project, is_active=False, **chat_data.model_dump()
        )

        return await ChatResponseScheme.from_tortoise_orm(new_chat)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.message)

    except Exception as _e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Chat not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
@paginate_decorator
async def read_all(
    request: Request,
    filters: ChatFilterSchema = Depends(),  # type: ignore
    paginator: Paginator = Depends(),
    sort_by: list[str] = Query([]),
    select: list[str] = Query([]),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        query = OrderBy.create(query=ChatModel.all(), sort_by=sort_by)

        if not current_user.is_admin:
            query = query.filter(project__owner=current_user)

        filterd_query = Filter.create(query=query, filters=filters)
        paginated_data = await paginator.paginate(filterd_query)
        selected_data = Select.create(
            query=paginated_data.paginated_result,
            select=select,
            model=ChatModel,
        )

        return await paginated_data.get_paginated_response(selected_data)

    except HTTPException as _e:
        if _e.status_code == 400:
            return {"error": _e.detail}
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/{id}/",
    response_model=ChatResponseScheme,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Chat not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def read(
    id: int,
    controller: ChatController = Depends(get_chat_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        chat = await controller.permission_to_access_chat(id, current_user)
        return await ChatResponseScheme.from_tortoise_orm(chat)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.message)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )


@router.put(
    "/{id}/",
    response_model=ChatResponseScheme,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Chat not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def update(
    id: int,
    data: ChatUpdate,
    controller: ChatController = Depends(get_chat_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        await controller.permission_to_access_chat(id, current_user)
        dict_data = data.model_dump()
        updated_project = await controller.update(id, dict_data)
        return await ChatResponseScheme.from_tortoise_orm(updated_project)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )


@router.delete(
    "/{id}/",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Chat not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def delete(
    id: int,
    controller: ChatController = Depends(get_chat_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        chat = await controller.permission_to_access_chat(id, current_user)

        await controller.delete(chat)
        return {"message": "Selected chat has been deleted successfully"}

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.message)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )
