from sqladmin import ModelView

from shared.database.models.sender import Sender


class SenderAdminView(ModelView, model=Sender):  # type: ignore
    column_list = [
        Sender.id,
        Sender.name,
        Sender.description,
    ]
