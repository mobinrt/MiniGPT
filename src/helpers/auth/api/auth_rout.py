from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.app.features.user.auth.usecase.auth_usecase import AuthUseCase
from src.app.features.user.auth.service.auth_service_imp import AuthServiceImp, oauth2_scheme
from src.app.features.user.auth.domain.auth_schemas import TokenDisplay, AccessTokenDisplay
from src.app.features.user.domain.user_schema import UserDisplay
from src.app.core.exception.auth_exceptions import InvalidCredentialsError
from src.app.core.exception.base_exception import BaseError
from src.app.core.enum.user_role import UserRole
from src.app.features.user.auth.service.rbac import role_required
from src.app.features.user.dependencies import get_auth_service, get_auth_usecase

router = APIRouter(tags=['authentication'])

@router.post('/token', response_model=TokenDisplay, status_code=status.HTTP_202_ACCEPTED)
async def login_for_access_token(data: OAuth2PasswordRequestForm = Depends(), auth_usecase: AuthUseCase = Depends(get_auth_usecase)):
    try:
        return await auth_usecase.get_token(data)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail='Invalid email or password', headers={'WWW-Authenticate': 'Bearer'})
    except BaseError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message
        )
    except Exception as _e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



@router.post('/refresh-token', response_model=AccessTokenDisplay)
async def refresh_access_token(token: str = Depends(oauth2_scheme), auth_usecase: AuthUseCase = Depends(get_auth_usecase)):
    try:
        return await auth_usecase.refresh_access_token(token)
    except BaseError:
        raise HTTPException(status_code=401, detail='Invalid refresh token', headers={'WWW-Authenticate': 'Bearer'})
    except Exception as _e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get('/read/users/me', response_model=UserDisplay)
async def read_users_me(token: str = Depends(oauth2_scheme), auth_usecase: AuthUseCase = Depends(get_auth_usecase)):
    try:
        return await auth_usecase.get_current_user(token)
    except BaseError:
        raise HTTPException(status_code=401, detail='Invalid token or user not found', headers={'WWW-Authenticate': 'Bearer'})
    except Exception as _e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/admin/dashboard")
@role_required(UserRole.ADMIN.value) 
async def admin_dashboard(token: str = Depends(oauth2_scheme)):
    try:
        return {"message": "Welcome to the admin dashboard!"}
    except BaseError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=e.message
        )
    except Exception as _e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/dev-login-token")
async def get_dev_token(auth_service: AuthServiceImp = Depends(get_auth_service)):
    id = -1 
    token = await auth_service.create_access_token(user_id=id, role=UserRole.DEV)

    return {"access_token": token, "token_type": "bearer"}