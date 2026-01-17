"""
WebSocket Real-Time Sync for Phase 5
Zero-cost real-time task updates to all connected clients
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Set
import json
import asyncio

class ConnectionManager:
    """Manages WebSocket connections for real-time sync"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        print(f"✅ WebSocket connected. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove disconnected WebSocket"""
        self.active_connections.discard(websocket)
        print(f"❌ WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        message_json = json.dumps(message)
        disconnected = set()
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                print(f"⚠️ WebSocket send error: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.active_connections.discard(conn)
    
    async def send_personal(self, message: dict, websocket: WebSocket):
        """Send message to specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"⚠️ WebSocket send error: {e}")
            self.disconnect(websocket)


# Global connection manager
manager = ConnectionManager()


def setup_websocket_sync(app, event_bus):
    """
    Setup WebSocket endpoint and subscribe to event bus
    
    Args:
        app: FastAPI application instance
        event_bus: SimpleEventBus to subscribe to
    """
    
    @app.websocket("/ws/tasks")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket endpoint for real-time task updates"""
        await manager.connect(websocket)
        
        try:
            while True:
                # Keep connection alive and listen for client messages
                data = await websocket.receive_text()
                # Could handle client commands here if needed
                print(f"📨 Received from client: {data}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)
    
    # Subscribe to event bus and broadcast to all clients
    def broadcast_task_event(event: dict):
        """Broadcast task events to all WebSocket clients"""
        asyncio.create_task(manager.broadcast({
            "type": "task_event",
            "event": event
        }))
    
    # Subscribe to all task events
    for event_type in ["TASK_CREATED", "TASK_UPDATED", "TASK_COMPLETED", "TASK_DELETED"]:
        event_bus.subscribe(event_type, broadcast_task_event)
    
    print("✅ WebSocket sync endpoint registered at /ws/tasks")
    print("✅ Event bus broadcasting to WebSocket clients")


# Frontend usage example:
"""
// JavaScript client code
const ws = new WebSocket('ws://your-backend/ws/tasks');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'task_event') {
        console.log('Task updated:', data.event);
        // Refresh task list or update specific task in UI
        refreshTaskList();
    }
};

ws.onopen = () => console.log('✅ Connected to task updates');
ws.onerror = (error) => console.error('WebSocket error:', error);
"""
