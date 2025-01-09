from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

# from src.config.redis import redis_client
from src.config import TORTOISE_ORM

async def lifespan(app: FastAPI):  
    try:  
        print("Initializing database...")  
        await Tortoise.init(config=TORTOISE_ORM)  
        await Tortoise.generate_schemas()  
        
        # await redis_client.ping()  
        # print("Redis connection successful.")  
 
        yield  

    except Exception as e:  
        print("Error during initialization:", e)  
        raise e   

    finally:   
        # await redis_client.close()  
        # print("Redis client connection closed.")  
        await Tortoise.close_connections()  
        print("Database connections closed.")


app = FastAPI(lifespan=lifespan)


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
