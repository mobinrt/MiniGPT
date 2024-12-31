from . import app


@app.get("/")
def start():
    return "this is my Mini GPT project!!"


