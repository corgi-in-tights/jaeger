import asyncio
import websockets
import json
from uuid import uuid4

SOCKET_IP = "ws://localhost:8765"

u = uuid4()


async def response_test(ip):
    async with websockets.connect(ip) as socket:
        msg = json.dumps({"_type": "queue_actor", "_id": str(u), "data": {"elo": 1000}})
        await socket.send(msg)
        res = await socket.recv()
        response = json.loads(res)

        print(response['_type'])

        await socket.wait_closed()

    

if __name__ == '__main__':
	asyncio.run(response_test(SOCKET_IP))