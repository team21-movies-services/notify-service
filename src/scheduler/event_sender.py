import logging

from celery import Celery

logger = logging.getLogger(__name__)


def send_notification(app: Celery, notification_content: dict):
    """
    Функция для отправки уведомления.
    """
    logger.info(f"Событие {notification_content} отправлено")
    app.send_task('send_notification', (notification_content,))
