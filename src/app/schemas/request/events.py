from pydantic import BaseModel


class IncomingEvent(BaseModel):
    event_name: str
    event_time: int
    event_data: dict | None
