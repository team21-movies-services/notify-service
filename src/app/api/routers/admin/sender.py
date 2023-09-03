from shared.database.models.sender import Sender
from sqladmin import ModelView


class SenderAdminView(ModelView, model=Sender):  # type: ignore
    column_list = [
        Sender.id,
        Sender.name,
        Sender.description,
    ]
