import json
from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_groups: Dict[str, List[str]] = {}
        self.group_members: Dict[str, List[str]] = {}
        self.group_remarks: Dict[str, Dict[str, str]] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections[username] = websocket
        print(f"{username} connected.")

    async def disconnect(self, username: str):
        self.active_connections.pop(username, None)
        for group in self.user_groups.get(username, []):
            if username in self.group_members.get(group, []):
                self.group_members[group].remove(username)
        self.user_groups.pop(username, None)
        print(f"{username} disconnected.")

    async def join_group(self, username: str, group: str, remark: str):
        self.user_groups.setdefault(username, []).append(group)
        self.group_members.setdefault(group, []).append(username)
        self.group_remarks.setdefault(group, {})[username] = remark
        print(f"{username} joined group {group}")

    async def leave_group(self, username: str, group: str):
        if group in self.user_groups.get(username, []):
            self.user_groups[username].remove(group)
        if username in self.group_members.get(group, []):
            self.group_members[group].remove(username)
        print(f"{username} left group {group}")

    async def call_group(self, username: str, group: str):
        members = self.group_members.get(group, [])
        for member in members:
            if member != username and member in self.active_connections:
                await self.active_connections[member].send_text(json.dumps({
                    "type": "call",
                    "from": username,
                    "group": group,
                    "remark": self.group_remarks.get(group, {}).get(username, "")
                }))
        print(f"{username} called group {group}")
