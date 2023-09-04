import json
import logging

from .config import settings

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = ["console"]


class CustomJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        super(CustomJsonFormatter, self).format(record)
        output = {k: str(v) for k, v in record.__dict__.items()}
        return json.dumps(output)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": LOG_FORMAT,
        },
        "json": {
            "()": lambda: CustomJsonFormatter(),
        },
    },
    "handlers": {
        "console": {
            "level": settings.project.log_level,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "json": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": settings.project.log_level,
        },
    },
    "root": {
        "level": settings.project.log_level,
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}
