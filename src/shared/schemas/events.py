from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, field_validator

from shared.enums.events import EventNameEnum


class EventSchema(BaseModel):
    event_name: EventNameEnum
    event_time: int
    event_data: EventUsersNewSchema | EventFilmsNewSchema

    @field_validator('event_data', mode='before')
    def set_event_data_type(cls, event_data, values):
        match values.data.get('event_name'):
            case EventNameEnum.users_created:
                event_data = EventUsersNewSchema(**event_data)
            case EventNameEnum.films_new:
                event_data = EventFilmsNewSchema(**event_data)
            case _ as unreachable:
                raise ValueError(f"Cannot set event data: {unreachable}")
        return event_data


class EventUsersNewSchema(BaseModel):
    user_id: UUID
    email: str


class EventFilmsNewSchema(BaseModel):
    film_id: UUID
