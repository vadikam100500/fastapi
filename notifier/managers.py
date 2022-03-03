from typing import Dict

from fastapi import WebSocket, WebSocketDisconnect

from db import add_to_sended, open_pool


class UserManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        try:
            await websocket.accept()
            self.active_connections[client_id] = websocket
        except WebSocketDisconnect:
            pass

    def disconnect(self, client_id: str):
        try:
            self.active_connections.pop(client_id)
        except KeyError:
            pass

    async def check_messages(self, websocket: WebSocket, client_id: str):
        conn_realtime = await open_pool()
        try:
            if data := await conn_realtime.hgetall(client_id):
                for date, message in data.items():
                    await websocket.send_text(f'{message}')
                    await conn_realtime.hdel(client_id, date)
                    await add_to_sended(conn_realtime, client_id,
                                        message, date)
        except WebSocketDisconnect:
            await conn_realtime.close()
            return
        else:
            await conn_realtime.close()


users_manager = UserManager()
