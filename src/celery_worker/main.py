import logging
import time

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from celery_worker.config import CeleryConfig
from celery_worker.connectors import PGConnect, SentryConnector, SyncPGConnect

time.sleep(2)

logger = logging.getLogger(__name__)
celery_config = CeleryConfig()


def create_app(config: CeleryConfig) -> Celery:
    app = Celery(
        config.app_name,
        broker=config.broker,
        backend=config.backend,
        config_source='shared.config.celery_config',
        include=[
            "celery_worker.tasks.notifications",
            "celery_worker.tasks.debug",
            "celery_worker.tasks.template",
        ],
    )

    return app


app = create_app(celery_config)
sentry_connect = SentryConnector()


@worker_process_init.connect
def init_worker(**kwargs):
    PGConnect.set(SyncPGConnect())
    sentry_connect.start_sentry()


@worker_process_shutdown.connect
def shutdown_worker(**kwargs):
    PGConnect.get().close()
    sentry_connect.shutdown_sentry()
