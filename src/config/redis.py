from redis.asyncio import Redis

redis_client = Redis(host="localhost", port=6380, decode_responses=True)


async def get_redis_client() -> Redis:
    return redis_client
