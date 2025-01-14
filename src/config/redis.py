from redis.asyncio import Redis

redis_client = Redis(host="localhost", port=6379, db=0)


async def get_redis_client() -> Redis:
    return redis_client
