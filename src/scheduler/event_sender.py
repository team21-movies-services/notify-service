import logging

from celery import Celery

logger = logging.getLogger(__name__)


def send_notification(app: Celery, notification_content: dict) -> None:
    """
    Функция для отправки уведомления.
    """
    logger.info("Событие %s отправлено", notification_content)
    app.send_task('send_notification', (notification_content,))
