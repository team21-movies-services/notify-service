from pydantic import BaseModel


class EventResponse(BaseModel):
    status: int
    data: dict
