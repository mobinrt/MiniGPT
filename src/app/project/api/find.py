from fastapi import HTTPException, status, Depends, Query, Request

from . import router
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.auth.rbac import get_role
from src.helpers.enum.user_role import UserRole
from src.helpers.auth import oauth2_scheme
from src.app.project.schema import ProjectDisplay
from src.app.project.controller import ProjectController, get_project_controller
from src.helpers.auth.dependencies import get_current_user
from src.app.user.model import UserModel
from src.app.project.model import ProjectModel

from src.helpers.filter import Filter
from src.helpers.pagination import Paginator, paginate_decorator
from src.helpers.order_by import OrderBy
from src.helpers.select import Select
from src.helpers.filter_schema import create_filter_schema

ProjectFilterSchema = create_filter_schema(
    ProjectModel,
    excludes=["created_at", "updated_at", "description"],
    filter_operations=["contains", "exact"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found any project"}},
)
@paginate_decorator
async def find_projects(
    request: Request,
    filters: ProjectFilterSchema = Depends(),  # type: ignore
    paginator: Paginator = Depends(),
    sort_by: list[str] = Query([]),
    select: list[str] = Query([]),
    token: str = Depends(oauth2_scheme),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        role = await get_role(token)
        query = OrderBy.create(query=ProjectModel.all(), sort_by=sort_by)

        if role == UserRole.MEMBER.value:
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
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/{id}",
    response_model=ProjectDisplay,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Project not found"}},
)
async def find_project_by_id(
    id: int,
    token: str = Depends(oauth2_scheme),
    current_user: UserModel = Depends(get_current_user),
    controller: ProjectController = Depends(get_project_controller),
):
    try:
        role = await get_role(token)
        project = await controller.get_by_id(id)
        project_owner = await project.owner

        if current_user != project_owner and role != UserRole.ADMIN.value:
            raise BaseError("Project not found")

        return ProjectDisplay.model_validate(project)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
