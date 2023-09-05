from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from src.shared.database.models.notification import Notification
from src.shared.database.models.schedule import Schedule


class EventsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_notification(self, event_name: str) -> Notification | None:
        """Получение notification по имени события"""

        query_result = await self._session.execute(select(Notification).where(Notification.event_name == event_name))

        notification = query_result.scalar_one_or_none()

        return notification

    async def create_schedule_event(self, notification_id: str, event_data: dict) -> UUID:
        time_delta = timedelta(hours=1)
        start_time = datetime.now() + time_delta
        schedule_event = Schedule(
            notification_id=notification_id,
            content=event_data,
            start_time=start_time,
        )
        self._session.add(schedule_event)
        await self._session.flush()
        schedule_event_id = schedule_event.id
        await self._session.commit()
        return schedule_event_id
