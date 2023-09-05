from celery_worker.main import app


@app.task(name="debug_task")
def add(x):
    return x
