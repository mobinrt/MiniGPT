from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError

from src.config import settings
from src.app.project.model import ProjectModel

class ActiveProjectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        if token:
            try: 
                payload = jwt.decode(token.split("Bearer ")[1], settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                active_project_id = payload.get("active_project_id")
                if active_project_id:
                    project = await ProjectModel.get_or_none(id=active_project_id)
                    if not project:
                        raise HTTPException(status_code=404, detail="Active project not found")
                    request.state.active_project = project
                else:
                    request.state.active_projecct = None
            except JWTError:
                raise HTTPException(status_code=403, detail="Invalid token")
        else:
            request.state.active_project = None
        
        return await call_next(request)