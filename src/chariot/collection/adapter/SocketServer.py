import asyncio
import json
from typing import Awaitable, List
import websockets
from websockets import WebSocketServer, WebSocketServerProtocol
from chariot.collection.adapter import DataOutputAdapter
from chariot.utility.JSONTypes import JSONObject


class SocketServer(DataOutputAdapter):
    def __init__(self, host: str = '0.0.0.0', port: int = 65432):
        super().__init__()
        self._host = host
        self._port = port
        self._running: bool = False

    def start(self) -> None:
        if self._running:
            return

        self._running = True
        run_serve: Awaitable[WebSocketServer] = websockets.serve(self._serve, host=self._host, port=self._port)
        asyncio.get_event_loop().run_until_complete(run_serve)

    async def _serve(self, websocket: WebSocketServerProtocol, path: str) -> Awaitable[None]:
        while self._running:
            record: List[JSONObject] = self._dataQueue.get()
            if record:
                recordJson = json.dumps(record)
                await websocket.send(recordJson)

    def stop(self) -> None:
        self._running = False
        self._dataQueue.put(None)
