from celery_worker.main import app


@app.task(name='send_notification')
def send_notification(notification_data):
    return notification_data
