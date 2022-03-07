import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from ..utils.db import PAST_KEY, open_pool
from .managers import users_manager
from .utils import get_user_id

router = APIRouter()


@router.websocket("/realtime")
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


@router.get("/messages/{client_id}")
async def user_sended_mess(client_id: str):
    """
    Return all client sended messages for the last month
    before last tournament.
    """
    conn = await open_pool()
    data = await conn.hget(PAST_KEY, client_id)
    await conn.close()
    return json.loads(data) if data else {'messages': 'no actual'}
