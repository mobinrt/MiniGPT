from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from src.config import settings


class ActiveProjectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token:
            try:
                payload = jwt.decode(
                    token.split("Bearer ")[1],
                    settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM],
                )
                active_project_id = payload.get("active_project_id")
                if active_project_id:
                    request.state.active_project_id = int(active_project_id)
                else:
                    request.state.active_project_id = None
            except JWTError:
                raise HTTPException(status_code=403, detail="Invalid token")
        else:
            request.state.active_project_id = None

        return await call_next(request)
