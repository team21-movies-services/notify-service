from sqladmin import ModelView

from models.sender import Sender


class SenderAdminView(ModelView, model=Sender):  # type: ignore
    column_list = [
        Sender.id,
        Sender.name,
        Sender.description,
    ]
