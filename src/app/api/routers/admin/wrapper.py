from sqladmin import ModelView

from shared.database.models.wrapper import Wrapper


class WrapperAdminView(ModelView, model=Wrapper):  # type: ignore
    column_list = [
        Wrapper.id,
        Wrapper.name,
    ]
