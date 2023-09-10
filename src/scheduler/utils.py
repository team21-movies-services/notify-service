import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


class BackoffException(Exception):
    pass


def gen_backoff(exceptions: tuple[type[Exception]], max_retries: int = 20, pause: int | float = 10):
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
                    logger.info("Ошибка в функции %s: %s. Повторная попытка через %s секунд.", func.__name__, e, pause)
                    if retry == retries:
                        raise BackoffException(
                            f"Превышено максимальное количество попыток для функции {func.__name__}.",
                        )
                    time.sleep(pause)

        return wrapper

    return decorator
