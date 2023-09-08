from typing import AsyncGenerator, Protocol
from uuid import UUID


class AMPQClientProtocol(Protocol):
    async def get_new_notifications(self, user_id: UUID) -> AsyncGenerator[str, None]:
        if False:  # hack for mypy
            yield
