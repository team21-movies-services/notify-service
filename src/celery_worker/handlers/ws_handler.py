import asyncio
import json
import logging
from dataclasses import dataclass
from functools import partial

import aio_pika
from jinja2 import DictLoader, Environment

from celery_worker.config import WebsocketProvidersConfig
from celery_worker.schemas.content import ContentListSchema
from celery_worker.schemas.users import UserInfoSchema
from shared.schemas.template import TemplateSchema

from .main import HandlerABC

logger = logging.getLogger(__name__)


@dataclass
class WebsocketHandler(HandlerABC):
    _config = WebsocketProvidersConfig()
    _connection = partial(aio_pika.connect_robust, _config.broker)

    def render(self, content: ContentListSchema, template: TemplateSchema) -> str:
        template_loader = DictLoader({"body": template.body})
        template_env = Environment(loader=template_loader, autoescape=True)
        template_render = template_env.from_string(template.body)
        rendered_template = template_render.render({"content": content})

        return rendered_template

    def send(self, users: list[UserInfoSchema], message: str, subject: str):
        asyncio.run(self._send(users, message, subject))

    async def _send(self, users: list[UserInfoSchema], message: str, subject: str):
        connection = await self._connection()

        data = {
            "subject": subject,
            "message": message,
        }

        async with connection:
            channel = await connection.channel()

            for user in users:
                routing_key = f"{self._config.queue_notify}:{user.id}"
                body = aio_pika.Message(body=json.dumps(data).encode('utf'))
                await channel.default_exchange.publish(body, routing_key, timeout=self._config.timeout)
