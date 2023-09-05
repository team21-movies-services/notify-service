from abc import ABC, abstractmethod

from celery import Celery

from core.exceptions.events import NotificationException
from repositories.events import EventsRepository
from schemas.request.events import IncomingEvent
from shared.database.models.notification import NotificationType


class EventsServiceABC(ABC):
    @abstractmethod
    async def handling_event(self, event_data: IncomingEvent):
        raise NotImplementedError


class EventsService(EventsServiceABC):
    def __init__(self, event_repository: EventsRepository, celery_app: Celery) -> None:
        self._event_repository = event_repository
        self._celery_app = celery_app

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
            self._celery_app.send_task('send_notification', (event_data.model_dump(),))
            return {'notification_type': NotificationType.instant, 'event_status': 'event has sent'}

        raise NotificationException
