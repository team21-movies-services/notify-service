import logging
import uuid
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import select

from shared.exceptions.base import ObjectDoesNotExist
from shared.database.models.template import Template
from shared.dto.templates import TemplateDto

logger = logging.getLogger(__name__)


class TemplatesRepositoryProtocol(Protocol):
    async def get(self, template_id: uuid.UUID) -> TemplateDto:
        ...


class TemplatesRepository(TemplatesRepositoryProtocol):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, template_id: uuid.UUID) -> TemplateDto:
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
        return TemplateDto.from_model(db_obj)
