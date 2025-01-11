from fastapi import HTTPException, status, Depends, Query, Request, APIRouter

from src.app.project.schema import ProjectCreate, ProjectUpdate
from src.app.project.controller import ProjectController, get_project_controller
from src.helpers.auth.dependencies import get_current_user
from src.app.user.model import UserModel
from src.app.project.model import ProjectModel

from src.helpers.schema import ProjectResponseScheme
from src.helpers.exceptions.entities import NotFoundError
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.filter import Filter
from src.helpers.pagination import Paginator, paginate_decorator
from src.helpers.order_by import OrderBy
from src.helpers.select import Select
from src.helpers.filter_schema import create_filter_schema

router = APIRouter(
    prefix="/project",
    tags=["project"],
)

ProjectFilterSchema = create_filter_schema(
    ProjectModel,
    excludes=["created_at", "updated_at", "description"],
    filter_operations=["contains", "exact"],
)


@router.post(
    "/",
    response_model=ProjectResponseScheme,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"}},
)
async def create(
    data: ProjectCreate,
    controller: ProjectController = Depends(get_project_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        project = await controller.create(owner=current_user, **data.model_dump())
        return await ProjectResponseScheme.from_tortoise_orm(project)

    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/all/",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found any project"}},
)
@paginate_decorator
async def read_all(
    request: Request,
    filters: ProjectFilterSchema = Depends(),  # type: ignore
    paginator: Paginator = Depends(),
    sort_by: list[str] = Query([]),
    select: list[str] = Query([]),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        query = OrderBy.create(query=ProjectModel.all(), sort_by=sort_by)

        if not current_user.is_admin:
            query = query.filter(owner=current_user)

        filterd_query = Filter.create(query=query, filters=filters)
        paginated_data = await paginator.paginate(filterd_query)

        selected_data = Select.create(
            query=paginated_data.paginated_result,
            select=select,
            model=ProjectModel,
        )
        return await paginated_data.get_paginated_response(selected_data)

    except HTTPException as _e:
        if _e.status_code == 400:
            return {"error": _e.detail}
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.get(
    "/{id}/",
    response_model=ProjectResponseScheme,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Project not found"}},
)
async def read(
    id: int,
    current_user: UserModel = Depends(get_current_user),
    controller: ProjectController = Depends(get_project_controller),
):
    try:
        project = await controller.get_by_id(id)
        project_owner = await project.owner

        if current_user != project_owner and not current_user.is_admin:
            raise BaseError("Project not found")

        return await ProjectResponseScheme.from_tortoise_orm(project)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    "/{id}/",
    response_model=ProjectResponseScheme,
    status_code=status.HTTP_200_OK,
)
async def update(
    id: int,
    data: ProjectUpdate,
    controller: ProjectController = Depends(get_project_controller),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        project = await controller.get_by_id(id)
        project_owner = await project.owner

        if current_user != project_owner:
            raise BaseError("Project not found")

        dict_data = data.model_dump()
        updated_project = await controller.update(id, dict_data)

        return await ProjectResponseScheme.from_tortoise_orm(updated_project)

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}/",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def delete(
    id: int,
    current_user: UserModel = Depends(get_current_user),
    controller: ProjectController = Depends(get_project_controller),
):
    try:
        project = await controller.get_by_id(id)
        project_owner = await project.owner

        if current_user != project_owner and not current_user.is_admin:
            raise NotFoundError()

        await controller.delete(project)
        return {"message": "Selected project has been deleted successfully"}

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
