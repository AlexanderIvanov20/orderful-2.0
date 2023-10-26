from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        await websocket.accept()

        self.connections.setdefault(user_id, websocket)

    def disconnect(self, user_id: int) -> None:
        self.connections.pop(user_id)

    async def notify(self, message: str, user_id: int) -> None:
        if websocket := self.connections.get(user_id):
            await websocket.send_text(message)


connection_manager = ConnectionManager()
