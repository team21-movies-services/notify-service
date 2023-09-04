import logging
from dataclasses import dataclass
from uuid import UUID

from requests import Session as RequestSession

from celery_worker.config import APIsConfig
from celery_worker.schemas.content import ContentListSchema, FilmsInfoSchema
from celery_worker.schemas.users import UserInfoList, UserInfoSchema
from shared.enums.events import EventNameEnum

logger = logging.getLogger(__name__)


@dataclass
class ContentService:
    _client: RequestSession
    _api: APIsConfig

    def get_users_info(self, event_name: EventNameEnum, user_id: UUID | None = None) -> UserInfoList:
        if user_id:
            response = self._client.get(self._api.users.info_uri.format(user_id=user_id))
        else:
            response = self._client.get(self._api.users.list_uri.format(event_name=event_name))
        return [UserInfoSchema(**user) for user in response.json()]

    def get_new_films_info(self, from_date: int) -> ContentListSchema:
        content_response = self._client.get(self._api.films.new_uri.format(date_after=from_date))
        return [FilmsInfoSchema(**film) for film in content_response.json()]
