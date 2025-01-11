from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
import asyncio
from src.config import TORTOISE_ORM

from src.app.link.task import app as clock_app


async def lifespan(app: FastAPI):
    try:
        print("Initializing database...")
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        aio_clock_task = asyncio.create_task(clock_app.serve())

        yield

    except Exception as e:
        print("Error during initialization:", e)
        raise e

    finally:
        if aio_clock_task:
            aio_clock_task.cancel()
            
            try:
                await aio_clock_task
            except asyncio.CancelledError:
                print("AioClock task cancelled.")
                
        await Tortoise.close_connections()
        print("Database connections closed.") 


app = FastAPI(lifespan=lifespan)


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
