import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from requests import Session as RequestSession
from celery_worker.config import APIsConfig

from shared.schemas.template import TemplateSchema
from celery_worker.schemas.content import ContentListSchema
from celery_worker.schemas.users import UserInfoSchema

from jinja2 import DictLoader, Environment


logger = logging.getLogger(__name__)


class HandlerABC(ABC):
    @abstractmethod
    def render(self, content: ContentListSchema, template: TemplateSchema) -> str:
        ...

    @abstractmethod
    def send(self, users: list[UserInfoSchema], message: str, subject: str):
        ...


@dataclass
class EmailHandlers(HandlerABC):
    _client = RequestSession()
    _api = APIsConfig()

    def render(self, content: ContentListSchema, template: TemplateSchema) -> str:
        template_loader = DictLoader({"body": template.body})
        template_env = Environment(loader=template_loader, autoescape=True)
        template_render = template_env.from_string(template.body)

        rendered_template = template_render.render({"content": content})
        if template.wrapper:
            template_render = template_env.from_string(template.wrapper.body)
            rendered_template = template_render.render({"content": rendered_template})

        return rendered_template

    def send(self, users: list[UserInfoSchema], message: str, subject: str):
        recipients = [user.email for user in users]
        data = {
            "recipients": recipients,
            "subject": subject,
            "message": message,
        }
        response = self._client.post(self._api.email_providers.send_email_uri(), data=data)
        logger.info(response)
