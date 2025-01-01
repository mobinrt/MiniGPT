from fastapi import status
from fastapi.responses import JSONResponse

from . import app
from src.helpers.exceptions.auth_exceptions import AccessDenied




@app.exception_handler(AccessDenied)
async def base_error_handler(request, exc: AccessDenied):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )

