import asyncio
import socket

class RSSocket:
    def __init__(self):
        self.socket = None
        self.connected = False

    async def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        try:
            await asyncio.get_running_loop().sock_connect(self.socket, (host, port))
            self.connected = True
            print("Connected")
        except Exception as e:
            print(f"Connection failed: {e}")
            self.connected = False

    async def send(self, data):
        if not self.connected:
            print("Socket is not connected.")
            return
        if isinstance(data, str):
            data = data.encode()
        await asyncio.get_running_loop().sock_sendall(self.socket, data)

    async def receive(self, bufsize=4096):
        if not self.connected:
            print("Socket is not connected.")
            return None
        data = await asyncio.get_running_loop().sock_recv(self.socket, bufsize)
        return data

    async def clear_available(self):
        """Read and discard data to 'clear' the socket. Use with caution."""
        if not self.connected:
            print("Socket is not connected.")
            return
        try:
            while True:
                # Attempt to read with a very small timeout to avoid blocking.
                data = await asyncio.wait_for(self.receive(4096), timeout=0.1)
                if not data:  # If no data is received, break the loop.
                    break
        except asyncio.TimeoutError:
            # Expected if no data is received within the timeout. Simply exit the method.
            pass
        except Exception as e:
            print(f"Error during clear_available: {e}")

    async def wait_for_data(self, timeout=None):
        """Wait for data to be available and return it."""
        if not self.connected:
            print("Socket is not connected.")
            return None
        try:
            data = await asyncio.wait_for(self.receive(4096), timeout=timeout)
            return data
        except asyncio.TimeoutError:
            print("Wait for data timed out.")
            return None
        except Exception as e:
            print(f"Error waiting for data: {e}")
            return None

    def close(self):
        if self.connected:
            self.socket.close()
            self.connected = False
            print("Socket closed")
