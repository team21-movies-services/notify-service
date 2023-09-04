from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Event(BaseModel):
    id: UUID
    crontab: str
    start_time: datetime
    completed: bool
    content: dict
    created_at: datetime
    updated_at: datetime
