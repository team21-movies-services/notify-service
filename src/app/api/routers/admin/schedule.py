from sqladmin import ModelView

from shared.database.models.schedule import Schedule


class ScheduleAdminView(ModelView, model=Schedule):  # type: ignore
    column_list = [
        Schedule.id,
        Schedule.crontab,
        Schedule.start_time,
        Schedule.completed,
        Schedule.notification_id,
    ]
