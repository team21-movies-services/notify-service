# notify-service

* link = https://github.com/team21-movies-services/notify-service

# Init development

1) init poetry and pre-commit
```bash
poetry install --no-root
```

```bash
poetry run pre-commit install
```

2) env
```bash
cp ./.env.template ./.env
```
* `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` - пользователь, пароль, название БД с которыми будет создана БД в postgres.

```bash
cp ./src/.env.template ./src/.env
```

* `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT` - настройки подключения к БД postgres

3) build and up docker local
```bash
make build-local
make up-local
```

# Migration

1) generate
```
cd src
poetry run alembic revision --autogenerate -m "message"
```

2) upgrade
```
$ poetry run alembic upgrade head
```

3) print sql
```
$ poetry run alembic upgrade head --sql
```
