import asyncio
from server import consumer_handler
import websockets
from config.settings import SOCKET_SETTINGS

async def heartbeat():
	while True:
		print ('heartbeat')
		await asyncio.sleep(5)

async def main():
	asyncio.create_task(heartbeat())

	# TODO specify ping_interval, ping_timeout, close_timeout, max_size, max_queue, read_limit, and write_limit in config
	server = await websockets.serve(
		consumer_handler, **SOCKET_SETTINGS
	)
	await server.wait_closed()

asyncio.run(main())