import logging
import uuid

from shared.database.models.template import Template
from shared.exceptions.base import ObjectDoesNotExist
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.sql import select

logger = logging.getLogger(__name__)


class TemplatesRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, template_id: uuid.UUID) -> Template:
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
        return db_obj
