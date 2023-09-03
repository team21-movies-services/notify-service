import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped

from models.base import Column


class IdMixin:
    __abstract__ = True

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        nullable=False,
        primary_key=True,
    )


class TsMixinCreated:
    __abstract__ = True

    created_at: Mapped[datetime] = Column(
        TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )


class TsMixinUpdated:
    __abstract__ = True

    updated_at: Mapped[datetime] = Column(
        TIMESTAMP(timezone=False),
        default=datetime.utcnow,
        nullable=False,
    )
