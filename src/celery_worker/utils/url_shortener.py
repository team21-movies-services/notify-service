import logging
from dataclasses import dataclass
from http import HTTPStatus

from requests import Session as RequestSession

from celery_worker.config import APIsConfig

logger = logging.getLogger(__name__)


@dataclass
class UrlShortenerService:
    _client: RequestSession
    _api: APIsConfig

    def get_short_url(self, long_url: str) -> str | None:
        request_json = {
            "url": long_url,
        }
        headers = {"Authorization": f"Bearer {self._api.tinyurl.token}"}
        result = self._client.post(self._api.tinyurl.shortener_uri, json=request_json, headers=headers)
        status = result.status_code
        body = result.json()
        match status:
            case HTTPStatus.OK:
                return body.get('data').get('tiny_url')
            case _:
                logger.error('Errors during making short url. List of errors: {}'.format(body.get('errors')))
                return None
