import json
import asyncio
import logging
from typing import List
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

router = APIRouter(tags=["WebSockets"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket client connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            logger.info("WebSocket client disconnected.")

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending WS message: {e}")


manager = ConnectionManager()


@router.websocket("/ws/rounds")
async def websocket_rounds(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and push simulated periodic telemetry heartbeat
            await asyncio.sleep(5)
            await websocket.send_json({
                "type": "TELEMETRY_HEARTBEAT",
                "timestamp": asyncio.get_event_loop().time(),
                "status": "HEALTHY"
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
