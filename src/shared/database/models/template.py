import uuid

from sqlalchemy import PrimaryKeyConstraint, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, relationship

from shared.database.models.base import BaseModel, Column, RestrictForeignKey
from shared.database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from shared.database.models.sender import Sender
from shared.database.models.wrapper import Wrapper


class Template(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.templates db table."""

    __tablename__ = "templates"
    __table_args__ = (
        PrimaryKeyConstraint('id', name='template_pkey'),
        {"schema": "public"},
    )

    name: Mapped[str] = Column(String(127), nullable=False, comment="Название шаблона")
    description: Mapped[str] = Column(String(255), nullable=False, comment="Описание шаблона")

    subject: Mapped[str] = Column(String(127), nullable=True, comment="Заголовок шаблона")
    body: Mapped[str] = Column(Text, nullable=False, comment="Тело шаблона")
    json_vars: Mapped[dict] = Column(JSONB, nullable=False, default={}, comment="Переменные шаблона")

    wrapper_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        RestrictForeignKey(Wrapper.id),
        nullable=False,
        comment="ID враппера",
    )
    sender_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        RestrictForeignKey(Sender.id),
        nullable=True,
        comment="ID отправителя",
    )

    wrapper: Mapped[Wrapper] = relationship()
    sender: Mapped[Sender] = relationship()

    def __str__(self) -> str:
        return f"{self.name} - {self.id}"
