import uvicorn
from src import app
from src.app.user.api.user_routers import user_router


@app.get("/")
def start():
    return "this is my Mini GPT project!!"


app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
