from fastapi import HTTPException, status, Depends, Request, Query, APIRouter

from src.app.chat.schema.prompt_schema import PromptCreate, PromptUpdate
from src.app.chat.controller.prompt_controller import get_prompt_controller, PromptController
from src.app.user.model import UserModel
from src.app.chat.model.message_model import PromptModel
from src.app.chat.model import ChatModel

from src.helpers.auth.dependencies import get_current_user
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.exceptions.entities import NotFoundError
from src.helpers.schema import PromptResponseScheme
from src.helpers.filter import Filter
from src.helpers.pagination import Paginator, paginate_decorator
from src.helpers.order_by import OrderBy
from src.helpers.select import Select
from src.helpers.filter_schema import create_filter_schema

router = APIRouter(
    prefix="/prompt",
    tags=["prompt"],
)

PromptFilterSchema = create_filter_schema(
    PromptModel,
    excludes=["created_at", "updated_at"],
    filter_operations=["contains", "exact"],
)

MessageFilterSchema = create_filter_schema(
    PromptModel,
    excludes=["created_at", "updated_at"],
    filter_operations=["contains", "exact"],
)


@router.post(
    "/",
    response_model=PromptResponseScheme,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"},
        status.HTTP_404_NOT_FOUND: {"description": "Chat not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def create(
    prompt_data: PromptCreate,
    controller: PromptController = Depends(get_prompt_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        active_chat = await ChatModel.get(id=prompt_data.chat_id)
        active_project = await active_chat.project
        user = await active_project.owner

        if user != current_user:
            raise NotFoundError()

        new_prompt = await controller.create(
            chat=active_chat, **prompt_data.model_dump()
        )
        return await PromptResponseScheme.from_tortoise_orm(new_prompt)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.message)

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )


@router.get(
    "/all/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Prompt not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
@paginate_decorator
async def read_all(
    request: Request,
    filters: PromptFilterSchema = Depends(),  # type: ignore
    paginator: Paginator = Depends(),
    sort_by: list[str] = Query([]),
    select: list[str] = Query([]),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        query = OrderBy.create(query=PromptModel.all(), sort_by=sort_by)

        if not current_user.is_admin:
            query = query.filter(chat__project__owner=current_user)

        filtered_query = Filter.create(query=query, filters=filters)
        paginated_data = await paginator.paginate(filtered_query)
        selected_data = Select.create(
            query=paginated_data.paginated_result,
            select=select,
            model=PromptModel,
        )

        return await paginated_data.get_paginated_response(selected_data)

    except HTTPException as _e:
        if _e.status_code == 400:
            return {"error": _e.detail}
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )


@router.get(
    "/{id}/",
    response_model=PromptResponseScheme,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Prompt not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def read(
    id: int,
    controller: PromptController = Depends(get_prompt_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        prompt = await controller.permission_to_access_prompt(id, current_user)
        return await PromptResponseScheme.from_tortoise_orm(prompt)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.message)
    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="An unexpected error occurred. Please try again later.",
    #     )


@router.put(
    "/{id}/",
    response_model=PromptResponseScheme,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Prompt not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def update(
    id: int,
    data: PromptUpdate,
    controller: PromptController = Depends(get_prompt_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        await controller.permission_to_access_prompt(id, current_user)
        dict_data = data.model_dump()
        updated_prompt = await controller.update(id, dict_data)
        return await PromptResponseScheme.from_tortoise_orm(updated_prompt)

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
        status.HTTP_404_NOT_FOUND: {"description": "Prompt not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def delete(
    id: int,
    controller: PromptController = Depends(get_prompt_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        prompt = await controller.permission_to_access_prompt(id, current_user)

        await controller.delete(prompt)
        return {"message": "Selected prompt has been deleted successfully"}

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.message)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        )


# @responce_router.post(
#     "/responces/",
#     response_model=ResponceModelResponseScheme,
#     status_code=status.HTTP_201_CREATED,
#     responses={
#         status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"},
#         status.HTTP_404_NOT_FOUND: {"description": "Prompt not found"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# async def create_responce(
#     responce_data: ResponceCreate,
#     controller: ResponceController = Depends(get_responce_controller),
#     current_user: UserModel = Depends(get_current_user),
# ):
#     try:
#         active_prompt = await controller.get_prompt_by_id(responce_data.prompt_id)
#         new_responce = await controller.create(
#             prompt=active_prompt, **responce_data.model_dump()
#         )
#         return await ResponceModelResponseScheme.from_tortoise_orm(new_responce)

#     except NotFoundError as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

#     except BaseError as ex:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.message)

#     except Exception:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An unexpected error occurred. Please try again later.",
#         )


# @responce_router.get(
#     "/responces/",
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Responce not found"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
# )
# @paginate_decorator
# async def read_all_responces(
#     request: Request,
#     filters: ResponceFilterSchema = Depends(),  # type: ignore
#     paginator: Paginator = Depends(),
#     sort_by: list[str] = Query([]),
#     select: list[str] = Query([]),
#     current_user: UserModel = Depends(get_current_user),
# ):
#     try:
#         query = OrderBy.create(query=ResponceModel.all(), sort_by=sort_by)

#         if not current_user.is_admin:
#             query = query.filter(prompt__chat__owner=current_user)

#         filtered_query = Filter.create(query=query, filters=filters)
#         paginated_data = await paginator.paginate(filtered_query)
#         selected_data = Select.create(
#             query=paginated_data.paginated_result,
#             select=select,
#             model=ResponceModel,
#         )

#         return await paginated_data.get_paginated_response(selected_data)

#     except HTTPException as _e:
#         if _e.status_code == 400:
#             return {"error": _e.detail}
#     except BaseError as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
#     except Exception as _e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @responce_router.get(
#     "/responces/{id}/",
#     response_model=ResponceModelResponseScheme,
#     status_code=status.HTTP_200_OK,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"description": "Responce not found"},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
#     },
