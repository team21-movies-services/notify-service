from aio_pika.connection import Connection
from fastapi import Depends

from app.core.config import Settings
from app.dependencies.clients.get_ampq_connection import get_ws_ampq_connection
from app.dependencies.registrator import add_factory_to_mapper
from app.dependencies.settings import get_settings
from app.services.queue_notify import QueueNotifyService, QueueNotifyServiceProtocol
from app.wrappers import AMPQIOPikaClient


@add_factory_to_mapper(QueueNotifyServiceProtocol)
def create_queue_notify_service(
    ampq_connection: Connection = Depends(get_ws_ampq_connection),
    settings: Settings = Depends(get_settings),
) -> QueueNotifyService:
    ampq_client = AMPQIOPikaClient(_connection=ampq_connection, _settings=settings.ampq)
    return QueueNotifyService(ampq_client)
