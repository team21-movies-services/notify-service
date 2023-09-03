from main import app


@app.task(name="debug_task")
def task(test_value):
    return test_value
