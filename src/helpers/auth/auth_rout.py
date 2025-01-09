from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import ValidationError
from fastapi.responses import JSONResponse

from . import oauth2_scheme
from .auth_usecase import AuthUseCase
from .controller import AuthController
from .schema import TokenDisplay, AccessTokenDisplay
from .rbac import role_required
from .dependencies import get_auth_controller, get_auth_usecase

from src.app.user.schema import UserDisplay
from src.helpers.exceptions.auth_exceptions import InvalidCredentialsError
from src.helpers.exceptions.auth_exceptions import BaseError
from src.helpers.enum.user_role import UserRole

router = APIRouter(tags=["authentication"])


@router.post(
    "/token", response_model=TokenDisplay, status_code=status.HTTP_202_ACCEPTED
)
async def login_for_access_token(
    data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
):
    try:
        token_data  =  await auth_usecase.get_token(data)
        headers = {"Authorization": f"Bearer {token_data.access_token}"}
        return JSONResponse(content=token_data.model_dump(), headers=headers)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email format."
        )


@router.post("/refresh-token", response_model=AccessTokenDisplay)
async def refresh_access_token(
    token: str = Depends(oauth2_scheme),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
):
    try:
        return await auth_usecase.refresh_access_token(token)
    except BaseError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/read/users/me", response_model=UserDisplay)
async def read_users_me(
    token: str = Depends(oauth2_scheme),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
):
    try:
        return await auth_usecase.get_current_user(token)
    except BaseError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token or user not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/admin/dashboard")
@role_required(UserRole.ADMIN.value)
async def admin_dashboard(token: str = Depends(oauth2_scheme)):
    try:
        return {"message": "Welcome to the admin dashboard!"}
    except BaseError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)
    except Exception as _e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/dev-login-token")
async def get_dev_token(auth_controller: AuthController = Depends(get_auth_controller)):
    id = -1
    token = await auth_controller.create_access_token(user_id=id, role=UserRole.DEV)

    return {"access_token": token, "token_type": "bearer"}
