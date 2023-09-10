from scheduler.event_sender import send_notification


def test_send_notification(celery_mock, caplog):
    notification_content = {"message": "Пример уведомления"}
    send_notification(celery_mock, notification_content)

    assert caplog.records[0].msg == "Событие %s отправлено"
    assert caplog.records[0].args == notification_content

    celery_mock.send_task.assert_called_once_with('send_notification', (notification_content,))
