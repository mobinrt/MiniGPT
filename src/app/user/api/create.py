from fastapi import HTTPException, status
from . import router

from src.app.user.schema import UserCreate, UserDisplay
from src.app.user.controller import create_user
from src.helpers.exceptions.base_exception import BaseError


@router.post(
    "/create",
    response_model=UserDisplay,
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"}},
)
async def create(data: UserCreate):
    try:
        new_user = await create_user(data.username, data.email, data.password)
        return UserDisplay.model_validate(new_user)
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from fastapi import HTTPException, status, Query, Depends, Request
# from . import router

# from src.app.user.schema import UserCreate, UserDisplay
# from src.app.user.controller import create_user
# from src.helpers.exceptions.base_exception import BaseError
# from src.helpers import Filter, OrderBy, Paginator, Select, create_filter_schema
# from src.app.user.models import User  # Assuming User is your Tortoise ORM model

# # Create a dynamic filter schema for the User model
# UserFilterSchema = create_filter_schema(User)


# @router.post(
#     "/create",
#     response_model=UserDisplay,
#     status_code=status.HTTP_201_CREATED,
#     responses={status.HTTP_400_BAD_REQUEST: {"description": "Invalid data"}},
# )
# async def create(data: UserCreate):
#     try:
#         new_user = await create_user(data.username, data.email, data.password)
#         return UserDisplay.model_validate(new_user)
#     except BaseError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
#     except Exception as _e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @router.get(
#     "/users",
#     response_model=dict,  # Adjust this to the appropriate response model if available
#     responses={status.HTTP_400_BAD_REQUEST: {"description": "Invalid query parameters"}},
# )
# async def get_users(
#     request: Request,
#     page: int = Query(1, ge=1),
#     limit: int = Query(10, le=100),
#     filters: UserFilterSchema = Depends(),  # Dynamically generated filter schema
#     sort_by: list[str] = Query([], description="Sort fields, e.g., ['-created_at']"),
#     select: list[str] = Query([], description="Fields to include in the response"),
#     paginator: Paginator = Depends(),
# ):
#     try:
#         # Apply sorting
#         query = OrderBy.create(User.all(), sort_by)

#         # Apply filtering
#         query = Filter.create(query, filters)

#         # Paginate results
#         paginated_results = await paginator.paginate(query)

#         # Apply field selection
#         data = Select.create(paginated_results.paginated_result, select, User)

#         # Return the paginated response
#         return await paginated_results.get_paginated_response(data)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="An unexpected error occurred.",
#         )
