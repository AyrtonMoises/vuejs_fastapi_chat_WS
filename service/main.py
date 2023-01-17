import json
from collections import defaultdict

from fastapi import FastAPI, WebSocket, BackgroundTasks #,Request, Depends

from starlette.websockets import WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware

from routers import router


app = FastAPI(
    title="Chat API",
    description="API para criação de usuário e salas para chat",
    version="1.0.0",
)

app.include_router(router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Notifier:
    """
        Manages chat room sessions and members along with message routing
    """

    def __init__(self):
        self.connections: dict = defaultdict(dict)
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            msg = message["message"]
            room_id = message["room_id"]
            await self._notify(msg, room_id)

    def get_members(self, room_id):
        try:
            return self.connections[room_id]
        except Exception:
            return None

    async def push(self, msg: str, room_id: int = None):
        message_body = {"message": msg, "room_id": room_id}
        await self.generator.asend(message_body)

    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if self.connections[room_id] == {} or len(self.connections[room_id]) == 0:
            self.connections[room_id] = []
        self.connections[room_id].append(websocket)
        print(f"CONNECTIONS : {self.connections[room_id]}")

    def remove(self, websocket: WebSocket, room_id: int):
        self.connections[room_id].remove(websocket)
        print(
            f"CONNECTION REMOVED\nREMAINING CONNECTIONS : {self.connections[room_id]}"
        )

    async def _notify(self, message: str, room_id: int):
        living_connections = []
        while len(self.connections[room_id]) > 0:

            websocket = self.connections[room_id].pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections[room_id] = living_connections


notifier = Notifier()


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, room_id, background_tasks: BackgroundTasks
):
    await notifier.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_text()
            d = json.loads(data)
            d["room_id"] = room_id

            room_members = (
                notifier.get_members(room_id)
                if notifier.get_members(room_id) is not None
                else []
            )
            if websocket not in room_members:
                print("SENDER NOT IN ROOM MEMBERS: RECONNECTING")
                await notifier.connect(websocket, room_id)

            await notifier._notify(f"{data}", room_id)
    except WebSocketDisconnect:
        notifier.remove(websocket, room_id)