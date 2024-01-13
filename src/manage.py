import asyncio
from server import consumer_handler
# from callbacks import attempt_match
import websockets
from config.settings import SOCKET_SETTINGS, MATCH_RETRY_SECONDS

from callbacks import process_queue_head

async def heartbeat():
	while True:
		await process_queue_head()
		await asyncio.sleep(MATCH_RETRY_SECONDS)

async def main():
	asyncio.create_task(heartbeat())

	# TODO specify ping_interval, ping_timeout, close_timeout, max_size, max_queue, read_limit, and write_limit in config
	server = await websockets.serve(
		consumer_handler, **SOCKET_SETTINGS
	)
	await server.wait_closed()

if __name__ == '__main__':
	asyncio.run(main())