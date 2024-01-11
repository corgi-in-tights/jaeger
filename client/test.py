import asyncio
import websockets

async def message():
    async with websockets.connect("ws://localhost:8765") as socket:
        msg = input("Write your message to the server: ")
        await socket.send(msg)
        print(await socket.recv())

    await message()

asyncio.get_event_loop().run_until_complete(message())