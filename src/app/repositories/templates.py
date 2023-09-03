import logging
import uuid
from typing import Protocol

from shared.database.models.template import Template
from shared.exceptions.base import ObjectDoesNotExist
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import select

from app.schemas.template import TemplateSchema

logger = logging.getLogger(__name__)


class TemplatesRepositoryProtocol(Protocol):
    async def get(self, template_id: uuid.UUID) -> TemplateSchema:
        ...


class TemplatesRepository(TemplatesRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, template_id: uuid.UUID) -> TemplateSchema:
        query = (
            select(Template)
            .where(Template.id == template_id)
            .join(Template.wrapper)
            .join(Template.sender)
            .options(contains_eager(Template.wrapper), contains_eager(Template.sender))
        )
        result = await self._session.execute(query)
        db_obj = result.scalars().first()
        if not db_obj:
            raise ObjectDoesNotExist
        return TemplateSchema.model_validate(db_obj)
