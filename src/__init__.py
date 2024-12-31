from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

from src.config import TORTOISE_ORM

async def lifespan(app: FastAPI):
    print("Initializing database...")
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    yield
    print("Closing database connection...")
    await Tortoise.close_connections()


app = FastAPI(lifespan=lifespan)


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
