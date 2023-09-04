from dataclasses import dataclass
from typing import Any, NoReturn, Protocol

from requests import Session as RequestSession

from celery_worker.config import APIsConfig
from celery_worker.exceptions.events import EventCouldNotBeHandled
from celery_worker.schemas.content import ContentListSchema, FilmsInfoSchema
from shared.schemas.events import EventFilmsNewSchema, EventSchema, EventUsersNewSchema


class ContentServiceProtocol(Protocol):
    def get_content(self, event: EventSchema) -> ContentListSchema:
        ...


@dataclass
class UserCreatedContentService(ContentServiceProtocol):
    _client: RequestSession
    _api: APIsConfig

    def get_content(self, _: EventSchema) -> ContentListSchema:
        # ничего не возвращает но в будущем может пригодиться, если шаблон изменится (неудачная попытка в s.O.l.i.d)

        return None


@dataclass
class NewFilmContentService(ContentServiceProtocol):
    _client: RequestSession
    _api: APIsConfig

    def get_content(self, event: EventSchema) -> ContentListSchema:
        response = self._client.get(self._api.films.new_uri.format(date_after=event.event_time))
        return [FilmsInfoSchema(**film) for film in response.json()]


def get_content_service(event: EventSchema) -> ContentServiceProtocol:
    client = RequestSession()
    api = APIsConfig()

    match event.event_data:
        case EventUsersNewSchema():  # type: ignore[misc]
            return UserCreatedContentService(client, api)
        case EventFilmsNewSchema():  # type: ignore[misc]
            return NewFilmContentService(client, api)
        case _ as unreachable:
            _asset_never(unreachable)


def _asset_never(event_name: Any) -> NoReturn:
    raise EventCouldNotBeHandled(event_name)
