from pydantic import BaseModel


class IncomingEvent(BaseModel):
    user_id: str
    event_name: str
    event_time: str
    event_data: dict | None
