import datetime as dt
from typing import Optional

from fastapi.responses import JSONResponse

from api.utils.sender import send_mess
from worker import send_later


async def mess_handler(client_id: str, message: str,
                       send_date: Optional[str] = None) -> JSONResponse:
    """
    Handler that check type of message and write to buffer,
    or send to client.

    I Hope that messages not repeating, because i don't validate them.
    """
    response = JSONResponse(status_code=201)
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
            return response
    await send_mess(client_id, message, send_date)
    return response
