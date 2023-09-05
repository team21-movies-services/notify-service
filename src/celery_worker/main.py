import logging
import time

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from celery_worker.connectors import PGConnect, SyncPGConnect

time.sleep(5)

logger = logging.getLogger(__name__)


def create_app() -> Celery:
    app = Celery(
        "notify",
        broker="pyamqp://guest:guest@notify-service-rabbitmq",
        backend="rpc://guest:guest@notify-service-rabbitmq",
        include=[
            "celery_worker.tasks.notifications",
            "celery_worker.tasks.debug",
            "celery_worker.tasks.template",
        ],
    )

    return app


app = create_app()


@worker_process_init.connect
def init_worker(**kwargs):
    PGConnect.set(SyncPGConnect())


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    PGConnect.get().close()
