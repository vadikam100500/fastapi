import json

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect

from db import PAST_KEY, open_pool
from handlers import mess_handler
from managers import users_manager
from schemas import Confirmation, Invite, Registration
from token_handler import get_user_id

app = FastAPI()


@app.post('/registration')
async def tournament_reg(reg: Registration,
                         client_id: str = Depends(get_user_id)):
    """
    Get messages of service x, for realtime sending, after user
    registration on tournament.
    """
    return await mess_handler(client_id, reg.message)


@app.post('/reg_confirm')
async def tournament_confirm(conf: Confirmation,
                             client_id: str = Depends(get_user_id)):
    """
    Get messages of service y, for delay sending (1 hour before tournament).
    """
    return await mess_handler(client_id, conf.message, conf.date)


@app.post('/tourn_invite')
async def tourn_invite(inv: Invite, client_id: str = Depends(get_user_id)):
    """
    Get messages of service z, for delay sending (on tournament begin).
    """
    return await mess_handler(client_id, inv.message, inv.date)


@app.websocket("/realtime")
async def user_accaunt(websocket: WebSocket,
                       client_id: str = Depends(get_user_id)):
    """Socket with online client."""
    await users_manager.connect(websocket, client_id)
    try:
        while True:
            await users_manager.check_messages(websocket, client_id)
            await websocket.receive_text()
    except WebSocketDisconnect:
        users_manager.disconnect(client_id)
    except RuntimeError:
        users_manager.disconnect(client_id)


@app.get("/messages/{client_id}")
async def user_sended_mess(client_id: str):
    """
    Return all client sended messages
    for the last month before last tournament.
    """
    conn = await open_pool()
    data = await conn.hget(PAST_KEY, client_id)
    await conn.close()
    return json.loads(data) if data else {'messages': 'no actual'}
