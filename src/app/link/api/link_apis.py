from fastapi import HTTPException, status, Depends, Request, Query, APIRouter
from datetime import datetime

from src.app.link.schema import LinkCreate
from src.app.link.controller import get_link_controller, LinkController
from src.app.user.model import UserModel
from src.app.link.model import LinkModel

from src.helpers.auth.dependencies import get_current_user
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.exceptions.entities import NotFoundError
from src.helpers.schema import LinkResponseScheme
from src.helpers.filter import Filter
from src.helpers.pagination import Paginator, paginate_decorator
from src.helpers.order_by import OrderBy
from src.helpers.select import Select
from src.helpers.filter_schema import create_filter_schema

router = APIRouter(
    prefix="/link",
    tags=["link"],
)

LinkFilterSchema = create_filter_schema(
    LinkModel,
    excludes=["created_at", "updated_at", "link_url"],
    filter_operations=["contains", "exact"],
)


@router.post(
    "/",
    response_model=LinkResponseScheme,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def create(
    link_data: LinkCreate,
    request: Request,
    controller: LinkController = Depends(get_link_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        base_url = str(request.base_url)[:-1]
        new_link = await controller.create(user=current_user, **link_data.model_dump())
        new_link.generate_link_url(base_url)
        await new_link.save()
        return await LinkResponseScheme.from_tortoise_orm(new_link)

    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)


@router.get(
    "/all/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Link not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
@paginate_decorator
async def read_all(
    request: Request,
    filters: LinkFilterSchema = Depends(),  # type: ignore
    paginator: Paginator = Depends(),
    sort_by: list[str] = Query([]),
    select: list[str] = Query([]),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        query = OrderBy.create(query=LinkModel.all(), sort_by=sort_by)
        query = query.filter(user=current_user)

        if not current_user.is_admin:
            query = query.filter(user=current_user)

        query = query.filter(expired_at__gte=datetime.now())

        filtered_query = Filter.create(query=query, filters=filters)
        paginated_data = await paginator.paginate(filtered_query)

        selected_data = Select.create(
            query=paginated_data.paginated_result,
            select=select,
            model=LinkModel,
        )

        return await paginated_data.get_paginated_response(selected_data)

    except HTTPException as _e:
        if _e.status_code == 400:
            return {"error": _e.detail}
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get(
    "/{id}/",
    response_model=LinkResponseScheme,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Link not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def read(
    id: int,
    controller: LinkController = Depends(get_link_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        link = await controller.get_by_id(id)
        link_owner = await link.user

        if link.is_expired:
            raise NotFoundError("Link has expired.")

        if current_user != link_owner and not current_user.is_admin:
            raise NotFoundError()

        return await LinkResponseScheme.from_tortoise_orm(link)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)
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
        status.HTTP_404_NOT_FOUND: {"description": "Link not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def delete(
    id: int,
    controller: LinkController = Depends(get_link_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        link = await controller.get_by_id(id)
        link_owner = await link.user

        if current_user != link_owner and not current_user.is_admin:
            raise NotFoundError()

        await controller.delete(link)
        return {"message": "Selected link has been deleted successfully"}

    except BaseError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.detail)


@router.get(
    "/shared/{unique_id}/",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Link not found"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Link has expired or is not public"
        },
    },
)
async def access_shared_link(
    unique_id: str,
    request: Request,
    controller: LinkController = Depends(get_link_controller),
):
    try:
        link = await controller.get_by_url(unique_id=unique_id)

        if link.is_expired:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This link has expired.",
            )

        if not link.is_public:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This link is not public.",
            )

        user_agent = request.headers.get("user-agent", "Unknown")
        ip_address = request.client.host
        await controller.log_link_usage(link, user_agent, ip_address)

        if link.project:
            return {"type": "project", "data": await link.project.to_dict()}
        elif link.chat:
            return {"type": "chat", "data": await link.chat.to_dict()}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No resource linked."
        )

    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
