"""
WebSocket connection manager for real-time updates
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
import asyncio


class WebSocketManager:
    """Manages WebSocket connections for real-time parking updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.user_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int = None):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        if user_id:
            self.user_connections[user_id] = websocket
    
    def disconnect(self, websocket: WebSocket, user_id: int = None):
        """Remove a WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if user_id and user_id in self.user_connections:
            del self.user_connections[user_id]
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send message to a specific connection"""
        await websocket.send_json(message)
    
    async def send_to_user(self, user_id: int, message: dict):
        """Send message to a specific user"""
        if user_id in self.user_connections:
            await self.user_connections[user_id].send_json(message)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
    
    async def broadcast_parking_update(self, parking_lot_id: int, slot_updates: dict):
        """Broadcast parking slot availability updates"""
        message = {
            "type": "parking_update",
            "parking_lot_id": parking_lot_id,
            "slots": slot_updates,
            "timestamp": asyncio.get_event_loop().time()
        }
        await self.broadcast(message)
    
    async def handle_websocket(self, websocket: WebSocket):
        """Handle WebSocket connection lifecycle"""
        await self.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                # Handle incoming messages if needed
                try:
                    message = json.loads(data)
                    # Process message based on type
                    if message.get("type") == "subscribe":
                        # Handle subscription to parking lot updates
                        pass
                except json.JSONDecodeError:
                    await self.send_personal_message(
                        {"error": "Invalid JSON"}, websocket
                    )
        except WebSocketDisconnect:
            self.disconnect(websocket)


websocket_manager = WebSocketManager()

