FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR opt/app
COPY src/scheduler/requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY src/scheduler .

ENTRYPOINT ["python", "main.py"]
