import asyncio
import socket

class RSSocket:
    def __init__(self):
        self.socket = None
        self.connected = False  # Track connection status

    async def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        try:
            await asyncio.get_running_loop().sock_connect(self.socket, (host, port))
            print("Connected")
            self.connected = True
        except Exception as e:
            print(f"Connection failed: {e}")
            self.connected = False

    async def send(self, data):
        if not self.connected:
            print("Socket is not connected.")
            return
        if isinstance(data, str):
            data = data.encode()  # Encode if data is string
        await asyncio.get_running_loop().sock_sendall(self.socket, data)

    async def receive(self, bufsize=4096):
        if not self.connected:
            print("Socket is not connected.")
            return None
        return await asyncio.get_running_loop().sock_recv(self.socket, bufsize)

    def close(self):
        if self.connected:
            self.socket.close()
            self.connected = False
            print("Socket closed")