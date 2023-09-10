from unittest.mock import patch

import pytest

from scheduler.utils import BackoffException, gen_backoff


def test_backoff_fail(caplog):
    pause = 10
    max_retries = 5
    err_msg = 'Test exception'

    @gen_backoff((Exception,), max_retries, pause)
    def gen_func():
        raise Exception(err_msg)

    with patch('time.sleep'):
        with pytest.raises(BackoffException):
            next(gen_func())

    assert caplog.records[0].msg == "Ошибка в функции %s: %s. Повторная попытка через %s секунд."
    assert caplog.records[0].args[0] == 'gen_func'
    assert caplog.records[0].args[1].args[0] == err_msg
    assert caplog.records[0].args[2] == pause
    assert len(caplog.records) == max_retries + 1


def test_backoff_success():
    test_result = 2

    @gen_backoff((Exception,))
    def some_func():
        yield test_result

    assert next(some_func()) == test_result
