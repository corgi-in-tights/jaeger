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
        return await socket.recv()

async def begin_tests():
    a = await response_test(SOCKET_IP)
    b = json.dumps({"_type": "accept", "_id": str(u), "description": "queue_actor"})
    print ("Respose Test:", a == b)
    if (a != b):
        print ("Recieved", a)
        print ("Expected", b)

    



if __name__ == '__main__':
	asyncio.run(begin_tests())