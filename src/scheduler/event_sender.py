import logging

from celery import Celery

logger = logging.getLogger(__name__)


def send_event(app: Celery, event: dict):
    """
    Функция для отправки события.
    """
    logger.info(f"Событие {event} отправлено")
    app.send_task('debug_task', (event,))
