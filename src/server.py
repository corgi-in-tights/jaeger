import json
from websockets import WebSocketServerProtocol

from config.models import QueueActorMessageType, DequeueActorMessageType, RemoveActorMessageType, ErrorResponse, AcceptResponse

from callbacks import queue_actor, dequeue_actor, remove_actor

from utils.socket_utils import send_response, has_type_and_id, convert_package_types

MESSAGE_TYPES = [
	QueueActorMessageType(queue_actor),
	DequeueActorMessageType(dequeue_actor),
	RemoveActorMessageType(remove_actor)
]


async def handle_message(websocket: WebSocketServerProtocol, content: str):
	try:
		package = json.loads(content)
		if (has_type_and_id(package)):
			for message_type in MESSAGE_TYPES:
				if (new_package := convert_package_types(package, message_type)):
					await send_response(
						websocket,
						await message_type.fetch_response(websocket=websocket, **new_package)
					)
					return

			await send_response(websocket, ErrorResponse('invalid_values'))

		else:
			await send_response(websocket, ErrorResponse('missing_type_or_id'))
			
	except json.JSONDecodeError:
		await send_response(websocket, ErrorResponse('invalid_json'))



async def consumer_handler(websocket: WebSocketServerProtocol, path: str):
	print (f'Connecting client from {websocket.remote_address} to server at {websocket.local_address}')
	async for message in websocket:
		await handle_message(websocket, message)