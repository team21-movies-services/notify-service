from shared.database.models.wrapper import Wrapper
from sqladmin import ModelView


class WrapperAdminView(ModelView, model=Wrapper):  # type: ignore
    column_list = [
        Wrapper.id,
        Wrapper.name,
    ]
