from sqladmin import ModelView

from shared.database.models.notification import Notification


class NotificationAdminView(ModelView, model=Notification):  # type: ignore
    column_list = [
        Notification.id,
        Notification.event_name,
        Notification.template_id,
        Notification.notification_type,
    ]
