import logging
from uuid import UUID

from celery_worker.connectors import SyncPGConnect
from celery_worker.main import app
from celery_worker.repositories import TemplatesRepository

logger = logging.getLogger(__name__)


@app.task(name="get_template")
def get_template(template_id: UUID):
    pg_connect = SyncPGConnect()
    repository = TemplatesRepository(session=next(pg_connect.get_db_session()))
    logger.info(repository.get(template_id))
    pg_connect.close()
