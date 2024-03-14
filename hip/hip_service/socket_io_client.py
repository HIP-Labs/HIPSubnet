import asyncio
import socketio


class SocketIOClient:
    def __init__(self):
        self.sio = socketio.AsyncClient()

    async def connect(self, url):
        await self.sio.connect(url)
        print(f"Connected to Socket.IO server at {url}")

    async def getRandomCompletion(self):
            """
            Retrieves a random completion from the Socket.IO server.

            Returns:
                dict: If connected to the Socket.IO server, returns a dictionary with the following schema:
                {
                    'id': int,
                    'prompt': str,
                    'response': str | None,
                    'created_at': str,
                    'updated_at': str,
                    'api_key_id': int
                }
                None: If not connected to any Socket.IO server.
            """
            if self.sio.connected:
                future = asyncio.Future()

                def callback(data):
                    future.set_result(data)

                await self.sio.emit("getRandomCompletion", callback=callback)
                return await future
            else:
                print("Not connected to any Socket.IO server. Call 'connect' first.")

    def on_acknowledgement(self, data):
        print("Received acknowledgement:", data)

    async def close(self):
        await self.sio.disconnect()
        print("Socket.IO connection closed.")
