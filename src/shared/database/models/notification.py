import uuid
from enum import StrEnum, auto

from sqlalchemy import PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, relationship

from shared.database.models.base import BaseModel, Column, RestrictForeignKey
from shared.database.models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from shared.database.models.template import Template


class NotificationType(StrEnum):
    instant = auto()
    scheduled = auto()
    periodic = auto()


class Notification(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.notification db table."""

    __tablename__ = "notifications"
    __table_args__ = (
        PrimaryKeyConstraint('id', name='notification_pkey'),
        {"schema": "public"},
    )

    event_name: Mapped[str] = Column(String(127), nullable=False, comment="Название события")
    template_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        RestrictForeignKey(Template.id),
        nullable=False,
        comment="ID шаблона",
    )
    notification_type: Mapped[str] = Column(
        ENUM(NotificationType, name="notification_type"),
        nullable=False,
        comment="Типы нотификаций",
    )

    template: Mapped[Template] = relationship()

    def __str__(self) -> str:
        return f"{self.event_name} - {self.notification_type} - {self.id}"
