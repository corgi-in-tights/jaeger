import asyncio
import json
import uuid
import redis
import websockets
from websockets import WebSocketServerProtocol

from config.models import Message, TYPE_KEY, ID_KEY
from config.settings import SOCKET_SETTINGS
from events import queue_actor, dequeue_actor, remove_actor



MESSAGE_TYPES = {
	'queue_actor': queue_actor,
	'dequeue_actor': dequeue_actor,
	'remove_actor': remove_actor
}

def finish_type(t):
	return f'finish_{t}'

def get_address(websocket):
	return f'{websocket.remote_address[0]}:{websocket.remote_address[1]}'


# guranteed to have a `_type` and `_id`
async def parse_message(websocket: WebSocketServerProtocol, message: Message):
	if (message._type in MESSAGE_TYPES):
		result = await MESSAGE_TYPES[message._type](message)
	else:
		result = 404

	to_package = {
		'type': finish_type(message._type),
		'_id': str(message._id),
		'status': result if result else 400
	}

	await send_message(websocket, to_package)



async def handle_message(websocket: WebSocketServerProtocol, message: Message):
	try:
		from_package = json.loads(message)
		if (TYPE_KEY in from_package and ID_KEY in from_package):
			try:
				_type = str(from_package[TYPE_KEY])
				_id = uuid.UUID(str(from_package[ID_KEY]))
				message = Message(_id, _type, **{k:v for k, v in from_package.items() if (not k in [TYPE_KEY, ID_KEY])})

				await parse_message(websocket, message)
			except ValueError:
				await send_error(websocket, 'bad_value_types')
		else:
			await send_error(websocket, 'no_type_or_id_provided')
			
	except json.JSONDecodeError:
		await send_error(websocket, 'invalid_json')

async def send_error(websocket: WebSocketServerProtocol, description: str, **kwargs):
	await send_message(websocket, { 'type': 'error', 'description': description, **kwargs })

async def send_message(websocket: WebSocketServerProtocol, to_package: dict):
	await websocket.send(json.dumps(to_package))

c = []

async def consumer_handler(websocket: WebSocketServerProtocol, path: str):
	print (f'Connecting client from {websocket.remote_address} to server at {websocket.local_address}')
	c.append(websocket)
	async for message in websocket:
		print (c)
		await handle_message(websocket, message)


async def main():
	# specify ping_interval, ping_timeout, close_timeout, max_size, max_queue, read_limit, and write_limit in config
	server = await websockets.serve(
		consumer_handler, **SOCKET_SETTINGS
	)
	
	await server.wait_closed()

if __name__ == '__main__':
	asyncio.run(main())