import asyncio
from config.models import AcceptResponse, FailResponse, Actor
from config.settings import MAX_QUEUE_SIZE
from uuid import UUID, uuid4
from rq import Queue, Worker
from redis import Redis
from functools import partial
from queue import Queue
from typing import List

from config.settings import ACTIVE_MATCH_RULE, ACTIVE_SORT_RULE, SORTED_SET_KEY

from utils.socket_utils import send_confirmation

actor_queue = Queue(maxsize=MAX_QUEUE_SIZE)
uuid_socket_map = {} # socket instances cannot be stored in a zset

redis_conn = Redis(host='localhost', port=6379, decode_responses=True)
# clear anything that was saved
redis_conn.delete(SORTED_SET_KEY)


matches = {}

async def queue_actor(websocket, _id: UUID, _type: str, data: dict) -> AcceptResponse:
	if (actor_queue.full()):
		return FailResponse('overflow', _id)
	
	print ('queuing actor', _id)

	actor = Actor(websocket=websocket, _id=_id, data=data, retry_index=0)
	await add_actor_to_queue(actor)

	uuid_socket_map[_id] = websocket

	k = ACTIVE_SORT_RULE.get_by_sort_key(actor)
	if (not k):
		return FailResponse('invalid_values', _id)
		
	redis_conn.zadd(SORTED_SET_KEY, {str(_id): k})

	return AcceptResponse(_type, _id)


async def add_actor_to_queue(actor: Actor):
	actor_queue.put(
		partial(attempt_match, actor=actor),
		block = True,
		timeout = 5
	)

async def dequeue_actor(websocket, _id: UUID, _type: str) -> AcceptResponse:
	return AcceptResponse(_type, 200, _id)

async def process_queue_head():
	if (actor_queue.qsize() > 1):
		f = actor_queue.get(block=True, timeout=5)
		await f()


async def attempt_match(actor: Actor):
	print ("ATTEMPTING:", actor._id)

	a = [(UUID(_id), score) for _id, score in redis_conn.zrange(SORTED_SET_KEY, 0, -1, withscores=True)]
	prefiltered = ACTIVE_MATCH_RULE.prefilter(actor, a)
	candidates = ACTIVE_MATCH_RULE.get_candidates(actor, prefiltered, 2)
	if (len(candidates) == 0): 
		actor.failed_index += 1
		add_actor_to_queue(actor)
	
	
	await send_confirmation(actor.websocket, actor._id, uuid4())
	# send confirmation to first candidate

	# start 30 second timer to confirm the status of both people
	# neither party has confirmed
		# both are removed from the queue
	# actor does not confirm, candidate confirms
		# actor is removed from queue, candidate has their denied counter increased
	# actor confirms, candidate does not confirm
		# actor has their RETRY_INDEX increased and is put back in queue, candidate is removed
	# both confirm
		# they are both removed from the queue and their room is removed
		# they are both send a MatchResponse with the new pubsub room
		# they again have 30 seconds to confirm that they have joined the pubsub channel
			# and confirm (again)
		# --both servers do their thing
		# if there is an error (bad move, etc), a BadMatchReply is sent to jaeger
			# and the match is terminated, timeout or forfeit causes them to lose
		# jaeger then calculates their new data (using the rewards rule) and sends it back
		# its upto the game servers to choose whatever to do with this new data
		# or if they use a custom rule, to set it from here directly


async def confirm_match(websocket, _id: UUID, _type: str) -> AcceptResponse:
	pass
