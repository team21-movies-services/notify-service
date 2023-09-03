import asyncio

from uuid import UUID
import time

from concurrent.futures import ThreadPoolExecutor

from celery import Celery

from celery_worker.connectors import AsyncPGConnect
from shared.database.repositories import TemplatesRepository

time.sleep(5)

app = Celery(
    "notify",
    broker="pyamqp://guest:guest@notify-service-rabbitmq",
    backend="rpc://guest:guest@notify-service-rabbitmq",
)

pg_connect = AsyncPGConnect()
_executor = ThreadPoolExecutor(1)


def sync_blocking():
    time.sleep(2)


async def async_with_executor(loop, template_repository, template_id):
    # run blocking function in another thread,
    # and wait for it's result:
    await loop.run_in_executor(_executor, sync_blocking)
    return await template_repository.get(template_id)


@app.task(name="debug_task")
def add(x, y):
    return x + y


@app.task(name="get_template")
def get_template(template_id: UUID):
    template_repository = TemplatesRepository(session=pg_connect.get_session())
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(async_with_executor(loop, template_repository, template_id))
    print('\n\n')
    print(result)
    print('\n\n')
    loop.close()
