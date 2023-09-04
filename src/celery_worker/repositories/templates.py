import logging
import uuid

from sqlalchemy.orm import Session, contains_eager
from sqlalchemy.sql import select

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
