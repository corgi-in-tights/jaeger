import asyncio
from config.models import Message, Actor
from config.settings import ACTIVE_MATCH_RULE

actor_queue = []


# def get_address(websocket):
# 	return f'{websocket.remote_address[0]}:{websocket.remote_address[1]}'


async def queue_actor(websocket, message: Message) -> int:
	# actor_queue.append(Actor(message._id, **message.data))
	print ('queuing actor', message._id)

	# asyncio.create_task(dequeue_actor(websocket, message))

	return 200


async def dequeue_actor(websocket, message: Message) -> int:
	await asyncio.sleep(5)
	print ('dequeuing actor', message._id)
	
	return 200

async def remove_actor(websocket, message: Message) -> int:
	print ('removing actor', message)
	
	return 200