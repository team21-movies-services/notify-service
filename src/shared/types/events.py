from __future__ import annotations

from typing import TypedDict

from shared.enums.events import EventNameEnum


class EventDict(TypedDict):
    event_name: EventNameEnum
    event_time: str
    event_data: EventUsersNewDict | EventFilmsNewDict


class EventUsersNewDict(TypedDict):
    user_id: str
    email: str


class EventFilmsNewDict(TypedDict):
    film_id: str
