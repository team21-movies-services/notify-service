from main import app


@app.task(name="debug_task")
def task(event):
    return event
