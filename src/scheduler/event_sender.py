import logging

from celery import Celery

from schemas import Event

logger = logging.getLogger(__name__)


def send_event(app: Celery, event: Event):
    """
    Функция для отправки события.
    """
    logger.info(f"Событие {event} отправлено")
    app.send_task('debug_task', (event,))
