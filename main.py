import uvicorn
from fastapi import status, Request
from fastapi.responses import JSONResponse

from src import app
from src.helpers.exceptions.entities import NotFoundError
from src.helpers.exceptions.auth_exceptions import AccessDenied
from src.app.user.api.routers import user_router
from src.app.project.api.routers import project_router
from src.app.link.api.routers import link_router
from src.app.chat.api.routers import chat_router, prompt_router, websocket_router
from src.helpers.auth.auth_rout import router as auth_router
from src.middleware.rate_limit import RateLimitMiddleware


app.add_middleware(RateLimitMiddleware)


@app.exception_handler(AccessDenied)
async def access_denied_handler(request: Request, exc: AccessDenied):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc.message)},
    )


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc.message)},
    )


@app.exception_handler(Exception)
async def general_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


# @app.exception_handler(RateLimitException)
# async def rate_limit_exception(request: Request, exc: RateLimitException):
#     return JSONResponse(
#         status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#         content={"detail": str(exc.detail)},
#     )


@app.middleware("http")
async def log_request(request: Request, call_next):
    print(f"Request path: {request.url.path}")
    return await call_next(request)


@app.get("/")
def start():
    return "this is my Mini GPT project!!"


app.include_router(user_router)
app.include_router(project_router)
app.include_router(chat_router)
app.include_router(prompt_router)
app.include_router(link_router)
app.include_router(websocket_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
