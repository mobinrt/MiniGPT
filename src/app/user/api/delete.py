from fastapi import HTTPException, status, Depends
from . import router

from src.app.user.model import UserModel
from src.app.user.controller import delete_user
from src.helpers.exceptions.entities import DeleteAdmin
from src.helpers.exceptions.base_exception import BaseError
from src.helpers.auth.rbac import role_required
from src.helpers.enum.user_role import UserRole
from src.helpers.auth.controller import oauth2_scheme
from src.helpers.auth.dependencies import get_current_user


@router.delete(
    "/me",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
@role_required(UserRole.MEMBER.value)
async def delete_user_self(
    token: str = Depends(oauth2_scheme),
    current_user: UserModel = Depends(get_current_user),
):
    try:
        await delete_user(user_id=current_user.id)
        return {"message": "Your account has been deleted successfully"}

    except DeleteAdmin as ex:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=ex.message
        )
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    "/{id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
@role_required(UserRole.ADMIN.value)
async def delete_user_by_admin(
    id: int,
    token: str = Depends(oauth2_scheme),
):
    try:
        await delete_user(id)
        return {"message": "User deleted successfully by admin"}

    except DeleteAdmin as ex:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=ex.message
        )
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @router.delete(
#     "/delete",
#     response_model=dict,
#     status_code=status.HTTP_200_OK,
# )
# async def delete_user_account(
#     id: int = None,  # Optional for self-deletion
#     token: str = Depends(oauth2_scheme),
#     current_user: UserModel = Depends(get_current_user),
# ):
#     try:
#         if id is None:
#             # Self-deletion
#             validate_role(current_user, UserRole.MEMBER.value)
#             await delete_user(user_id=current_user.id)
#             return {"message": "Your account has been deleted successfully"}

#         else:
#             # Admin-deletion
#             validate_role(current_user, UserRole.ADMIN.value)
#             await delete_user(id)
#             return {"message": f"User with ID {id} deleted successfully by admin"}

#     except DeleteAdmin as ex:
#         # Specific exception handling
#         raise HTTPException(
#             status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=ex.message
#         )
#     except BaseError as e:
#         # Application-level errors
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
#     except Exception as _e:
#         # Unexpected errors
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
