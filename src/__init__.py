from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
import asyncio
from src.config import TORTOISE_ORM

from src.config.aioclock import app as clock_app, delete_expired_links, delete_expired_websocket_sessions


async def start_clock():
    print("Starting AioClock...")
    await clock_app.serve()


async def lifespan(app: FastAPI):
    aio_clock_task = None
    try:
        print("Initializing database...")
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()

        print("Running delete_expired_links task immediately...")
        await delete_expired_links()

        print("Running delete_expired_websocket_sessions task immediately...")
        await delete_expired_websocket_sessions()
        
        aio_clock_task = asyncio.create_task(start_clock())
        print("AIOClock is working")
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
