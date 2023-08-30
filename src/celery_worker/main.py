import time
from celery import Celery

time.sleep(15)

app = Celery(
    "notify",
    broker="pyamqp://guest:guest@notify-service-rabbitmq",
    backend="rpc://guest:guest@notify-service-rabbitmq",
)


@app.task(name="debug_task")
def add(x, y):
    return x + y
