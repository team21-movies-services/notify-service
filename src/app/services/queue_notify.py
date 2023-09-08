from dataclasses import dataclass
from typing import AsyncGenerator, Protocol
from uuid import UUID

from app.wrappers.ampq import AMPQClientProtocol


class QueueNotifyServiceProtocol(Protocol):
    async def get_new_messages(self, user_id: UUID) -> AsyncGenerator[str, None]:
        if False:  # hack for mypy
            yield


@dataclass
class QueueNotifyService(QueueNotifyServiceProtocol):
    _ampq_client: AMPQClientProtocol

    async def get_new_messages(self, user_id: UUID) -> AsyncGenerator[str, None]:
        async for message in self._ampq_client.get_new_notifications(user_id):
            yield message
