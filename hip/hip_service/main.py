import asyncio
from socket_io_client import SocketIOClient

async def main():
    client = SocketIOClient()
    await client.connect("wss://hipservice-production.up.railway.app")

    # Example usage
    res = await client.getRandomCompletion()
    print("Received response:", res)
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
