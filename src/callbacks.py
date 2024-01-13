import asyncio
from config.models import AcceptResponse, FailResponse
from config.settings import MAX_QUEUE_SIZE
from uuid import UUID
from rq import Queue, Worker
from redis import Redis
from functools import partial



actor_queue = []

async def queue_actor(websocket, _id: UUID, _type: str, data: dict) -> AcceptResponse:
	if (len(actor_queue) > MAX_QUEUE_SIZE):
		return FailResponse('overflow', _id)
	
	print ('queuing actor', _id)

	# asyncio.create_task(add_to_redis(websocket, _id, data))
	 
	# Enqueue a job
	actor_queue.append(partial(attempt_match, websocket=websocket, _id=_id, data=data))


	return AcceptResponse(_type, _id)


async def add_to_redis(websocket, _id: UUID, data: dict):
	# add to queue
	# add to elo sorted list
	pass



async def dequeue_actor(websocket, _id: UUID, _type: str) -> AcceptResponse:
	return AcceptResponse(_type, 200, _id)

async def remove_actor(websocket, _id: UUID, _type: str) -> AcceptResponse:
	return AcceptResponse(_type, 200, _id)

async def process_queue_head():
	print ('heartbeat')
	if (len(actor_queue) > 1):
		print ('yes')
		await actor_queue.pop(0)()


async def attempt_match(websocket, _id: UUID, data: dict):
	print ("I AM ATTEMPTING A MATCH FOR", _id)
	# get all actors from the redis queue
	# the first actor in the queue will be the one waiting the longest
	# so we pop them off

	# the actor has an "elo block" and a "retry attempt" which defines their range
	# (custom INITIATE rule is used for this)
	
	# we quickly iterate up and down picking a maximum of N other actors
	

	# we now do some comparisons to pick out an ordered list of N potential candidates
	# (custom MATCH rule is used for this)




async def match_candidates(actor, candidates):
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