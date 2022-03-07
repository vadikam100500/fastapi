from typing import Optional

from fastapi import WebSocketDisconnect

from ..messages.utils import add_to_send, add_to_sended
from ..users.managers import users_manager
from .db import open_pool


async def send_mess(client_id: str, message: str,
                    date: Optional[str] = None) -> None:
    """
    Send message to client socket and write mess to db as sended,
    if client online, else write to db to send later.
    """
    conn_realtime = await open_pool()

    if client_id in users_manager.active_connections:
        try:
            client_websocket = users_manager.active_connections[client_id]
            await client_websocket.send_text(message)
            await add_to_sended(conn_realtime, client_id, message, date)
        except WebSocketDisconnect:
            await add_to_send(conn_realtime, client_id, message, date)
    else:
        await add_to_send(conn_realtime, client_id, message, date)

    await conn_realtime.close()
