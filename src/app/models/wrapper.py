from sqlalchemy import PrimaryKeyConstraint, String, Text
from sqlalchemy.orm import Mapped

from models.base import BaseModel, Column
from models.mixins import IdMixin, TsMixinCreated, TsMixinUpdated


class Wrapper(BaseModel, IdMixin, TsMixinCreated, TsMixinUpdated):
    """Data model for public.wrappers db table."""

    __tablename__ = "wrappers"
    __table_args__ = (
        PrimaryKeyConstraint('id', name='wrapper_pkey'),
        {"schema": "public"},
    )

    name: Mapped[str] = Column(String(127), nullable=False, comment="Название враппера")
    body: Mapped[str] = Column(Text, nullable=False, comment="Тело враппера")
