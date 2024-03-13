import asyncio
import socket

class RSSocket:
    def __init__(self, address_family, socket_type, protocol_type):
        self.address_family = address_family
        self.socket_type = socket_type
        self.protocol_type = protocol_type
        self.socket = socket.socket(self.address_family, self.socket_type, self.protocol_type)
        self.m_stop = False
        self.m_closed = False
        self.m_asyncAvailable = 0
        self.UserObject = None

    async def connect(self, host, port):
        await self.loop.sock_connect(self.socket, (host, port))
        self.socket.setblocking(False)
        print("Connected")

    async def send(self, data):
        if self.m_closed:
            return
        await self.loop.sock_sendall(self.socket, data)
        print("Data sent")

    async def receive(self):
        if self.m_closed:
            return
        data = await self.loop.sock_recv(self.socket, 4096)  # Adjust buffer size as needed
        self.m_asyncAvailable = len(data)
        print("Data received")
        return data

    def close(self):
        self.socket.close()
        self.m_closed = True
        print("Socket closed")

    def run(self, host, port):
        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(self.connect(host, port))
            # The loop for send/receive operations can be added here
        finally:
            self.loop.close()


