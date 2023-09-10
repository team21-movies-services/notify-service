from typing import AsyncGenerator
from uuid import UUID

from app.services.queue_notify import QueueNotifyServiceProtocol


class QueueNotifyServiceMock(QueueNotifyServiceProtocol):
    async def get_new_messages(self, user_id: UUID) -> AsyncGenerator[str, None]:
        yield "No new notifications"


def get_queue_notify_service_mock() -> QueueNotifyServiceMock:
    return QueueNotifyServiceMock()
