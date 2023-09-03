from sqlalchemy import PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped

from models.base import BaseModel, Column
from models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class Sender(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.senders db table."""

    __tablename__ = "senders"
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sender_pkey'),
        {"schema": "public"},
    )

    name: Mapped[str] = Column(String(127), nullable=False, comment="Имя отправителя")
    description: Mapped[str] = Column(String(255), nullable=False, comment="Описание отправителя")

    def __str__(self) -> str:
        return f"{self.name} - {self.id}"
