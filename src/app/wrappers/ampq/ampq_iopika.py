import asyncio
import logging
from dataclasses import dataclass
from typing import AsyncGenerator
from uuid import UUID

from aio_pika.connection import Connection
from aio_pika.exceptions import QueueEmpty

from app.core.config import AMPQConfig

from .base import AMPQClientProtocol

logger = logging.getLogger(__name__)


@dataclass
class AMPQIOPikaClient(AMPQClientProtocol):
    _connection: Connection
    _settings: AMPQConfig

    async def get_new_notifications(self, user_id: UUID) -> AsyncGenerator[str, None]:
        channel = await self._connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(self._settings.queue_notify + f":{user_id}")

        try:
            while message := await queue.get():
                yield message.body.decode("utf-8")
                await message.ack()
                await asyncio.sleep(0.1)
        except QueueEmpty:
            yield "No new notifications"
        finally:
            await channel.close()
