import asyncio
from config.models import Message
from config.settings import ACTIVE_MATCH_RULE


async def queue_actor(message: Message) -> int:
	# Add the package to the Redis queue
	# redis_conn.lpush('processing_queue', json.dumps(package))
	print ('queuing actor', message)
	
	return 200


async def dequeue_actor(message: Message) -> int:
	print ('dequeuing actor', message)
	
	return 200


async def remove_actor(message: Message) -> int:
	print ('removing actor', message)
	
	return 200


