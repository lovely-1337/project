import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.host = host
        self.port = port
        self.db = db
        self.redis = None

    async def connect(self):
        self.redis = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )

        await self.redis.ping()

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.aclose()

