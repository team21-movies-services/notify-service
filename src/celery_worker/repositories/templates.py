import logging
import uuid

from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.sql import and_, select

from celery_worker.connectors import SyncPGConnect
from shared.database.models.notification import Notification
from shared.database.models.template import Template
from shared.exceptions.base import ObjectDoesNotExist
from shared.schemas.template import TemplateSchema

logger = logging.getLogger(__name__)


class TemplatesRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, template_id: uuid.UUID) -> TemplateSchema:
        query = (
            select(Template)
            .where(Template.id == template_id)
            .join(Template.wrapper)
            .join(Template.sender)
            .options(contains_eager(Template.wrapper), contains_eager(Template.sender))
        )
        result = self._session.execute(query)
        db_obj = result.scalars().first()
        if not db_obj:
            raise ObjectDoesNotExist
        return TemplateSchema.model_validate(db_obj)

    def get_by_event_and_notify(self, event_name: str, template_type: str) -> TemplateSchema:
        query = (
            select(Template)
            .where(Template.template_type == template_type)
            .join(Template.wrapper)
            .join(Template.sender)
            .join(Notification, and_(Notification.template_id == Template.id, Notification.event_name == event_name))
            .options(contains_eager(Template.wrapper), contains_eager(Template.sender))
        )
        result = self._session.execute(query)
        db_obj = result.scalars().first()
        if not db_obj:
            raise ObjectDoesNotExist
        return TemplateSchema.model_validate(db_obj)


def get_templates_repository(pg_connect: SyncPGConnect) -> TemplatesRepository:
    return TemplatesRepository(session=next(pg_connect.get_db_session()))
