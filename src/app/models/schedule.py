import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import BOOLEAN, JSONB, UUID
from sqlalchemy.orm import Mapped

from models.base import BaseModel, Column, RestrictForeignKey
from models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated
from models.notification import Notification


class Schedule(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.schedule db table."""

    __tablename__ = "schedule"
    __table_args__ = (
        PrimaryKeyConstraint('id', name='schedule_pkey'),
        {"schema": "public"},
    )

    crontab: Mapped[str] = Column(String(127), nullable=True, comment="Шаблон расписания")
    start_time: Mapped[datetime] = Column(TIMESTAMP(timezone=False), nullable=True, comment="Время старта нотификации")
    completed: Mapped[bool] = Column(BOOLEAN, nullable=False, default=False, comment="Флаг завершения расписания")
    content: Mapped[dict] = Column(JSONB, nullable=False, default='{}', comment="Содержимое нотификации")

    notification_id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        RestrictForeignKey(Notification.id),
        nullable=False,
        comment="ID нотификации",
    )
