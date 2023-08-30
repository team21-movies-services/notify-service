FROM python:3.11-slim

# Основной путь приложения
ENV SRC_DIR=/opt

# Путь до приложения celery
ENV APP_DIR=$SRC_DIR/app

ENV APP_USER=celery-user

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Создание no-root пользователя
RUN groupadd -r $APP_USER && \
    useradd -d $SRC_DIR -r -g $APP_USER $APP_USER && \
    chown $APP_USER:$APP_USER -R $SRC_DIR

USER $APP_USER

# Установка зависимостей
WORKDIR $SRC_DIR

ENV PATH="/$SRC_DIR/.local/bin:${PATH}"
RUN pip install --user --upgrade pip && \
    pip install --user --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
RUN poetry install --no-root --only main

WORKDIR $APP_DIR

# Копирования кода приложения
COPY ./src/celery_worker $APP_DIR

COPY infra/celery/entrypoint.sh /usr/local/bin/entrypoint.sh