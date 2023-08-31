from dataclasses import dataclass

from sqladmin import ModelView
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


@dataclass
class Notification(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)


class NotificationAdminView(ModelView, model=Notification):  # type: ignore
    ...
