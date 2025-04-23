from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from manager import ConnectionManager
import uvicorn
import json

app = FastAPI()
manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可按需设置来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            action = message.get("action")
            group = message.get("group")
            remark = message.get("remark", "")

            if action == "join":
                await manager.join_group(username, group, remark)
            elif action == "leave":
                await manager.leave_group(username, group)
            elif action == "call":
                await manager.call_group(username, group)
    except WebSocketDisconnect:
        await manager.disconnect(username)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
