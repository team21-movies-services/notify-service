import time

from celery import Celery

time.sleep(15)

app = Celery(
    "notify",
    broker="pyamqp://guest:guest@notify-service-rabbitmq",
    backend="rpc://guest:guest@notify-service-rabbitmq",
    include=["tasks.debug", "tasks.email"],
)
