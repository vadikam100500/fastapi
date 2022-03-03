import datetime as dt
from typing import Optional

from fastapi import WebSocketDisconnect
from fastapi.responses import JSONResponse

from db import add_to_send, add_to_sended, open_pool
from managers import users_manager
from worker import send_later


async def send_mess(client_id: str, message: str,
                    date: Optional[str] = None) -> None:
    """
    Send message to client socket, end write mess to db as sended,
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


async def mess_handler(client_id: str, message: str,
                       send_date: Optional[str] = None) -> JSONResponse:
    """
    Handler that check type of message and write to buffer,
    or send to client.

    I Hope that messages not repeating, because i don't validate them.
    """
    if send_date:
        # UTC datetime
        try:
            date_as_dt = dt.datetime.strptime(send_date,
                                              '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return JSONResponse(content={'desc': 'uncorrect date'},
                                status_code=400)
        if date_as_dt > dt.datetime.now():
            send_later.apply_async((client_id, message, send_date),
                                   eta=date_as_dt)
        else:
            await send_mess(client_id, message, send_date)
    else:
        await send_mess(client_id, message)

    return JSONResponse(status_code=201)
