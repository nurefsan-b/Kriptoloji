from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from cipher import CryptoMethods
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict, sender: WebSocket):
        for connection in self.active_connections:
            if connection != sender:
                await connection.send_text(json.dumps(message))

class CryptoServer:
    def __init__(self):
        self.app = FastAPI()
        self.crypto = CryptoMethods()
        self.manager = ConnectionManager()
        self.templates = Jinja2Templates(directory="templates")
        self.setup_routes()
        self.setup_static()

    def setup_static(self):
        self.app.mount("/static", StaticFiles(directory="static"), name="static")

    def setup_routes(self):
        @self.app.get("/")
        async def client_page(request: Request):
            return self.templates.TemplateResponse("client.html", {"request": request})

        @self.app.get("/server")
        async def server_page(request: Request):
            return self.templates.TemplateResponse("server.html", {"request": request})

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.manager.connect(websocket)
            try:
                await self.handle_websocket_connection(websocket)
            except WebSocketDisconnect:
                self.manager.disconnect(websocket)

        @self.app.get("/decrypt")
        async def decrypt_message(method: str, cipher_text: str, key: str):
            return await self.handle_decryption(method, cipher_text, key)

    async def handle_websocket_connection(self, websocket: WebSocket):
        while True:
            data = await websocket.receive_text()
            await self.process_message(json.loads(data), websocket)

    async def process_message(self, data: Dict, websocket: WebSocket):
        if data.get('encrypted'):
            data = await self.encrypt_message(data)
        await self.manager.broadcast(data, websocket)

    async def encrypt_message(self, data: Dict) -> Dict:
        encrypted_message = self.crypto.encrypt(
            data['method'],
            data['message'],
            data['key']
        )
        data['encrypted_message'] = encrypted_message
        data['original_message'] = data['message']
        return data

    async def handle_decryption(self, method: str, cipher_text: str, key: str) -> Dict:
        try:
            decrypted_message = self.crypto.decrypt(method, cipher_text, key)
            return {"decrypted_message": decrypted_message}
        except Exception as e:
            return {"error": str(e)}

# Create server instance
server = CryptoServer()
app = server.app