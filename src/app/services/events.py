from abc import ABC, abstractmethod

from celery_worker.main import add
from core.exceptions.events import NotificationException
from repositories.events import EventsRepository
from schemas.request.events import IncomingEvent
from shared.database.models.notification import NotificationType


class EventsServiceABC(ABC):
    @abstractmethod
    async def handling_event(self, event_data: IncomingEvent):
        raise NotImplementedError


class EventsService(EventsServiceABC):
    def __init__(self, event_repository: EventsRepository) -> None:
        self._event_repository = event_repository

    async def handling_event(self, event_data: IncomingEvent) -> dict | None:
        notification = await self._event_repository.get_notification(event_name=event_data.event_name)

        if not notification:
            return None

        if notification.notification_type == NotificationType.scheduled:
            schedule_event = await self._event_repository.create_schedule_event(
                event_data=event_data,
                notification_id=notification.id,
            )
            schedule_event_data = {'notification_type': NotificationType.scheduled, 'schedule_event_id': schedule_event}
            return schedule_event_data

        elif notification.notification_type == NotificationType.instant:
            # TODO Разобраться, как правильно отправить event в селери и поменять return
            await add()
            return {'notification_type': NotificationType.instant, 'task_status': 'task added'}

        raise NotificationException
