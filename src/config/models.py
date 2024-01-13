from config.base import BaseMessageType, BaseResponse, DATA_KEY

class AcceptResponse(BaseResponse):
    def __init__(self, description, _id=None) -> None:
        super().__init__('accept', description, _id=_id)
    
class ErrorResponse(BaseResponse):
    def __init__(self, description, _id=None) -> None:
        super().__init__('error', description, _id=_id)

    
class FailResponse(BaseResponse):
    def __init__(self, description, _id=None) -> None:
        super().__init__('fail', description, _id=_id)


class QueueActorMessageType(BaseMessageType):
    _type = 'queue_actor'

    def __init__(self, callback) -> None:
        types = {
            DATA_KEY: dict
        }

        super().__init__('queue_actor', callback, types=types)


class DequeueActorMessageType(BaseMessageType):
    def __init__(self, callback) -> None:
        super().__init__('dequeue_actor', callback)


class RemoveActorMessageType(BaseMessageType):
    def __init__(self, callback) -> None:
        super().__init__('remove_actor', callback)