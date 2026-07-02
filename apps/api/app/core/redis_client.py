"""Redis client for caching and pub/sub."""

import json
from typing import Any, Optional
import redis.asyncio as aioredis
from app.core.config import settings


class RedisClient:
    def __init__(self):
        self._client: Optional[aioredis.Redis] = None

    async def connect(self):
        self._client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
        await self._client.ping()

    async def disconnect(self):
        if self._client:
            await self._client.close()

    @property
    def client(self) -> aioredis.Redis:
        if not self._client:
            raise RuntimeError("Redis not connected")
        return self._client

    async def get(self, key: str) -> Optional[Any]:
        value = await self.client.get(key)
        if value:
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return value
        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = settings.REDIS_CACHE_TTL,
    ) -> bool:
        serialized = json.dumps(value) if not isinstance(value, str) else value
        return await self.client.setex(key, ttl, serialized)

    async def delete(self, key: str) -> int:
        return await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        return bool(await self.client.exists(key))

    async def publish(self, channel: str, message: Any) -> int:
        serialized = json.dumps(message) if not isinstance(message, str) else message
        return await self.client.publish(channel, serialized)

    async def get_pubsub(self):
        return self.client.pubsub()

    async def increment(self, key: str, amount: int = 1) -> int:
        return await self.client.incrby(key, amount)

    async def expire(self, key: str, ttl: int) -> bool:
        return await self.client.expire(key, ttl)

    async def hset(self, name: str, key: str, value: Any) -> int:
        return await self.client.hset(name, key, json.dumps(value))

    async def hget(self, name: str, key: str) -> Optional[Any]:
        value = await self.client.hget(name, key)
        if value:
            return json.loads(value)
        return None

    async def hgetall(self, name: str) -> dict:
        data = await self.client.hgetall(name)
        return {k: json.loads(v) for k, v in data.items()}


redis_client = RedisClient()
