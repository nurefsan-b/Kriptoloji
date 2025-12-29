from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import io
from cipher import CryptoMethods
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.sessions: Dict[WebSocket, Dict] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.sessions[websocket] = {}

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        if websocket in self.sessions:
            del self.sessions[websocket]

    def set_session_data(self, websocket: WebSocket, key: str, value):
        if websocket in self.sessions:
            self.sessions[websocket][key] = value

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
        
        from Klasik_Kripto.rsa import rsa_anahtar_uret
        self.server_public_key, self.server_private_key = rsa_anahtar_uret(512)
        print(f"Sunucu RSA Anahtarları Üretildi: Public={self.server_public_key}")

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

        @self.app.get("/get-server-public-key")
        async def get_server_public_key():
            return {
                "public_key": [str(x) for x in self.server_public_key]
            }

        @self.app.get("/decrypt")
        async def decrypt_message(method: str, cipher_text: str, key: str, implementation: str = 'manual'):
            return await self.handle_decryption(method, cipher_text, key, implementation)

        @self.app.post("/upload-encrypt")
        async def upload_encrypt(
            file: UploadFile = File(...),
            method: str = Form(...),
            key: str = Form(...)
        ):
            content = await file.read()
            
            try:
                text_content = content.decode('utf-8')
            except UnicodeDecodeError:
                if method == 'aes':
                    text_content = content
                else:
                    return {"error": "Binary files only supported with AES"}

            try:
                encrypted = self.crypto.encrypt(method, text_content, key)
            except Exception as e:
                return {"error": str(e)}
            
            return StreamingResponse(
                io.BytesIO(encrypted.encode('utf-8')),
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename=encrypted_{file.filename}.txt"}
            )

        @self.app.post("/upload-decrypt")
        async def upload_decrypt(
            file: UploadFile = File(...),
            method: str = Form(...),
            key: str = Form(...)
        ):
            content = await file.read()
            
            try:
                text_content = content.decode('utf-8')
            except UnicodeDecodeError:
                return {"error": "Input file must be a text file containing the ciphertext"}

            try:
                decrypted = self.crypto.decrypt(method, text_content, key)
            except Exception as e:
                return {"error": str(e)}
        
            filename = f"decrypted_{file.filename.replace('encrypted_', '').replace('.txt', '')}.txt"
            return StreamingResponse(
                io.BytesIO(decrypted.encode('utf-8')),
                media_type="application/octet-stream",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        @self.app.post("/send-file")
        async def send_file(
            file: UploadFile = File(...),
            method: str = Form(...),
            key: str = Form(...)
        ):
            content = await file.read()
            
            try:
                try:
                    text_content = content.decode('utf-8')
                except UnicodeDecodeError:
                    if method == 'aes':
                        text_content = content
                    else:
                        return {"error": "Binary files only supported with AES"}

                encrypted_content = self.crypto.encrypt(method, text_content, key)
                filename = f"encrypted_{file.filename}.txt"
                filepath = f"static/uploads/{filename}"
                

                mode = "wb"
                if isinstance(encrypted_content, str):
                    write_content = encrypted_content.encode('utf-8')
                else:
                    write_content = encrypted_content
                
                with open(filepath, mode) as f:
                    f.write(write_content)
                

                msg = {
                    'type': 'new_file',
                    'filename': filename,
                    'method': method,
                    'key': key, 
                    'url': f"/static/uploads/{filename}",
                    'original_name': file.filename
                }
                for connection in self.manager.active_connections:
                     try:
                        await connection.send_text(json.dumps(msg))
                     except Exception as e:
                        print(f"Broadcast error to {connection}: {e}")

                return {"status": "File sent and encrypted successfully"}

            except Exception as e:
                return {"error": str(e)}

        @self.app.get("/decrypt-download")
        async def decrypt_download(filename: str, method: str, key: str):
            try:
                filepath = f"static/uploads/{filename}"
                with open(filepath, "rb") as f:
                    encrypted_bytes = f.read()
                
                try:
                    encrypted_content = encrypted_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    encrypted_content = encrypted_bytes

                decrypted = self.crypto.decrypt(method, encrypted_content, key)
                
                orig_name = filename.replace("encrypted_", "").replace(".txt", "")
                
                if isinstance(decrypted, str):
                    out_bytes = decrypted.encode('utf-8')
                else:
                    out_bytes = decrypted

                return StreamingResponse(
                    io.BytesIO(out_bytes),
                    media_type="application/octet-stream",
                    headers={"Content-Disposition": f"attachment; filename=decrypted_{orig_name}"}
                )

            except Exception as e:
                return {"error": str(e)}

        @self.app.get("/generate-rsa-keys")
        async def generate_rsa_keys():
            from Klasik_Kripto.rsa import rsa_anahtar_uret
            public_key, private_key = rsa_anahtar_uret(512) 
            return {
                "public_key": [str(x) for x in public_key],
                "private_key": [str(x) for x in private_key]
            }

        from pydantic import BaseModel
        class DSASignRequest(BaseModel):
            message: str

        class DSAVerifyRequest(BaseModel):
            message: str
            signature_r: str
            signature_s: str
            public_key_x: str = None
            public_key_y: str = None

        @self.app.post("/dsa/sign")
        async def dsa_sign(request: DSASignRequest):
            from Klasik_Kripto.dsa import ECDSAManager
            from Klasik_Kripto.ecc import EllipticCurve
            
            dsa = ECDSAManager()
            priv_key, pub_key = EllipticCurve.generate_keypair()
            
            signature = dsa.sign(priv_key, request.message)
            return {
                "signature_r": str(signature[0]),
                "signature_s": str(signature[1]),
                "public_key_x": str(pub_key[0]),
                "public_key_y": str(pub_key[1])
            }

        @self.app.post("/dsa/verify")
        async def dsa_verify(request: DSAVerifyRequest):
            from Klasik_Kripto.dsa import ECDSAManager
            dsa = ECDSAManager()
            
            try:
                if request.public_key_x and request.public_key_y:
                    pub_key = (int(request.public_key_x), int(request.public_key_y))
                else:
                    return {"valid": False, "status": "Public Key Gerekli"}
                    
                signature = (int(request.signature_r), int(request.signature_s))
                is_valid = dsa.verify(pub_key, request.message, signature)
                
                return {
                    "valid": is_valid, 
                    "status": "İmza Doğrulandı" if is_valid else "Geçersiz İmza"
                }
            except Exception as e:
                 return {"valid": False, "status": f"Hata: {str(e)}"}

    async def handle_websocket_connection(self, websocket: WebSocket):
        while True:
            data = await websocket.receive_text()
            await self.process_message(json.loads(data), websocket)

    async def process_message(self, data: Dict, websocket: WebSocket):
        msg_type = data.get('type')
        
        if msg_type == 'handshake':
            await self.handle_handshake(data, websocket)
            return

        if data.get('encrypted'):
            await self.log_decrypted_message(data)
        else:
            method = data.get('method')
            message = data.get('message')
            key = data.get('key', '')
            
            if method and message:
                try:
                    encrypted_text = self.crypto.encrypt(method, message, key)
                    data['message'] = encrypted_text
                    data['encrypted'] = True
                    print(f"\n--- [SUNUCU] Klasik Şifreleme Yapıldı ---")
                    print(f"Yöntem: {method}")
                    print(f"Plaintext: {message}")
                    print(f"Ciphertext: {encrypted_text}")
                    print("-----------------------------------------\n")
                except Exception as e:
                    print(f"Sunucu şifreleme hatası: {e}")
                    data['server_error'] = str(e)
            
        await self.manager.broadcast(data, websocket)

    async def handle_handshake(self, data: Dict, websocket: WebSocket):
        try:
            client_pub_x = int(data.get('public_key_x'))
            client_pub_y = int(data.get('public_key_y'))
            client_pub = (client_pub_x, client_pub_y)
            
            priv_s, pub_s = self.crypto.generate_ecc_keypair()
            secret = self.crypto.compute_ecdh_secret(priv_s, client_pub)
            self.manager.set_session_data(websocket, 'shared_secret', secret)
            
            response = {
                'type': 'handshake_response',
                'public_key_x': str(pub_s[0]),
                'public_key_y': str(pub_s[1])
            }
            await websocket.send_text(json.dumps(response))
        except Exception as e:
            print(f"Handshake error: {e}")
            await websocket.send_text(json.dumps({'error': 'Handshake failed'}))

    async def log_decrypted_message(self, data: Dict):
        try:
            method = data['method']
            cipher_text = data['message']
            key_param = data['key']
            implementation = data.get('implementation', 'manual')
            
            if method == 'rsa':
                print(f"[HYBRID RSA] Decrypting Session Key...")
                from Klasik_Kripto.rsa import rsa_desifre_metin
                try:
                    session_key = rsa_desifre_metin(key_param, self.server_private_key)
                    print(f"[HYBRID RSA] Decrypted Session Key: {session_key}")
                    
                    decrypted = self.crypto.decrypt('aes', cipher_text, session_key, implementation)
                    
                    print(f"\n--- [SUNUCU LOG] RSA Hybrid Mesajı Alındı ---")
                    print(f"Encrypted Key: {key_param[:20]}...")
                    print(f"Decrypted Session Key: {session_key}")
                    print(f"Ciphertext: {cipher_text}")
                    print(f"DECRYPTED MESSAGE: {decrypted}")
                    print("----------------------------------------------\n")
                    data['decrypted_message'] = decrypted
                    return
                except Exception as e:
                     print(f"[HYBRID RSA] Error: {e}")
                     return

            decrypted = self.crypto.decrypt(
                method,
                cipher_text,
                key_param,
                implementation
            )
            print(f"\n--- [SUNUCU LOG] Şifreli Mesaj Alındı ---")
            print(f"Yöntem: {method} ({implementation})")
            print(f"Ciphertext: {cipher_text}")
            print(f"Key: {key_param}")
            print(f"DECRYPTED: {decrypted}")
            print("-----------------------------------------\n")
            data['decrypted_message'] = decrypted
            
        except Exception as e:
            print(f"Sunucu Çözme Hatası: {e}")
            data['server_error'] = str(e)

    async def handle_decryption(self, method: str, cipher_text: str, key: str, implementation: str = 'manual') -> Dict:
        import time
        try:
            start_time = time.time()
            decrypted_message = self.crypto.decrypt(method, cipher_text, key, implementation)
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            
            return {
                "decrypted_message": decrypted_message,
                "duration_ms": f"{duration_ms:.4f}"
            }
        except Exception as e:
            return {"error": str(e)}

server = CryptoServer()
app = server.app