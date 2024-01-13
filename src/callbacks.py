import asyncio
from config.models import AcceptResponse, FailResponse, Actor
from config.settings import MAX_QUEUE_SIZE
from uuid import UUID
from rq import Queue, Worker
from redis import Redis
from functools import partial
from queue import Queue
from typing import List

from config.settings import ACTIVE_MATCH_RULE, ACTIVE_SORT_RULE, SORTED_SET_KEY


actor_queue = Queue(maxsize=MAX_QUEUE_SIZE)
uuid_socket_map = {}

redis_conn = Redis(host='localhost', port=6379, decode_responses=True)
redis_conn.delete(SORTED_SET_KEY)

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
	print ("I AM ATTEMPTING A MATCH FOR", actor._id)
	# the actor has an "elo block" and a "retry attempt" which defines their range
	# (custom INITIATE rule is used for this)

	a = [(UUID(_id), score) for _id, score in redis_conn.zrange(SORTED_SET_KEY, 0, -1, withscores=True)]
	prefiltered = ACTIVE_MATCH_RULE.prefilter(actor, a)
	candidates = ACTIVE_MATCH_RULE.get_candidates(actor, prefiltered, 2)
	
	await match_candidates(actor, candidates)




async def match_candidates(actor: Actor, candidates: List[UUID]):
	# now we confirm which all of the candidate actors are online
	# by sending a ConfirmationResponse to their websockets
	# and expecting back a 'yes'
	# this happens one-by-one instead of mass sending confirms so people dont get cheated lol

	# if the candidate does not accept in time, we remove them from the queue and elo pool
	# and we increase the actors (not candidates) retry attempt (which pushes them
	# further down in the queue). a FailResponse of 'actor_timeout' is also sent back

	# if either the actor accepts or the candidate accepts in time but the other doesnt
	# we dont decrease the retry attempt as heavily, it just means one of them sucks
	# but the other is a good boi?

	# if both the actor and candidate accept within X seconds, we send a MatchResponse
	# with the redis pubsub channel id. both servers confirm again when they connect to it.

	# jaeger is not part of the pubsub, the only way to communicate w it is through
	# the websocket. so timeouts and forfeits go through that.

	# this means we are trusting each server individually to not spoof stuff :<
	# but i cant be bothered to make jaeger be a helicopter parent
	pass