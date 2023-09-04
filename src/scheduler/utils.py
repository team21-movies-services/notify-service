import logging
from functools import wraps
from time import sleep

logger = logging.getLogger(__name__)


class BackoffException(Exception):
    pass


def gen_backoff(exceptions: tuple[type[Exception]], max_retries: int = 20, pause: int = 10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = max_retries
            for retry in range(retries + 1):
                try:
                    gen = func(*args, **kwargs)
                    for i in gen:
                        yield i
                    break
                except exceptions as e:
                    logger.info(f"Ошибка в функции {func.__name__}: {e}. Повторная попытка через {pause} секунд.")
                    if retry == retries:
                        raise BackoffException(
                            f"Превышено максимальное количество попыток для функции {func.__name__}.",
                        )
                    sleep(pause)

        return wrapper

    return decorator
