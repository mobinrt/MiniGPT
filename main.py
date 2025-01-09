import uvicorn
from fastapi import status
from fastapi.responses import JSONResponse

from src import app
from src.helpers.exceptions.auth_exceptions import AccessDenied
from src.app.user.api.routers import user_router
from src.app.project.api.routers import project_router
from src.app.chat.api.routers import chat_router
from src.app.chat.message.api.routers import message_router
from src.helpers.auth.auth_rout import router as auth_router


@app.exception_handler(AccessDenied)
async def base_error_handler(request, exc: AccessDenied):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )


@app.get("/")
def start():
    return "this is my Mini GPT project!!"



app.include_router(user_router)
app.include_router(project_router)
app.include_router(chat_router)
app.include_router(message_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
