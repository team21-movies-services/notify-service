from typing import AsyncGenerator

from aio_pika.connection import Connection
from fastapi import FastAPI, WebSocket


async def get_ws_ampq_connection(websocket: WebSocket) -> AsyncGenerator[Connection, None]:
    app: FastAPI = websocket.app
    connection: Connection = app.state.ampq_connection
    yield connection
