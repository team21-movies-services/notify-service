import logging

from fastapi import APIRouter, Depends, HTTPException, status

from schemas.request.events import IncomingEvent
from schemas.response.events import EventResponse
from services.events import EventsServiceABC

router = APIRouter(prefix="/events", tags=["Events"])

logger = logging.getLogger().getChild("events-router")


@router.post(
    "",
    summary="Обработка входящего события",
    response_model=EventResponse,
)
async def handling_event(event_data: IncomingEvent, status_service: EventsServiceABC = Depends()) -> EventResponse:
    event = await status_service.handling_event(event_data=event_data)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Notification not found',
        )
    return EventResponse(status=status.HTTP_200_OK, data=event)
