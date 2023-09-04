from pydantic import BaseModel


class IncomingEvent(BaseModel):
    event_name: str
    event_time: str
    event_data: dict | None
