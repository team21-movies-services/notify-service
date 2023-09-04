from __future__ import annotations

from pydantic import BaseModel

from shared.enums.events import EventNameEnum


class EventSchema(BaseModel):
    event_name: EventNameEnum
    event_time: str
    event_data: EventUsersNewSchema | EventFilmsNewSchema


class EventUsersNewSchema(BaseModel):
    user_id: str
    email: str


class EventFilmsNewSchema(BaseModel):
    film_id: str
