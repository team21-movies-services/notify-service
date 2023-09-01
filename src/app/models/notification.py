import uuid

import auto
import StrEnum
from sqlalchemy import PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped

from models.base import BaseModel, Column
from models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


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
    template_id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), nullable=False, comment="ID шаблона")
    notification_type: Mapped[str] = Column(
        ENUM(NotificationType, name="action_type"),
        nullable=False,
        comment="Типы нотификаций",
    )
