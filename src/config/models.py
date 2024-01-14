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

class ConfirmMatchResponse(BaseResponse):
    def __init__(self, _id=None) -> None:
        super().__init__('confirm', 'match', _id=_id)



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


class ConfirmMatchMessageType(BaseMessageType):
    def __init__(self, callback) -> None:
        super().__init__('confirm_match', callback)



class Actor:
    def __init__(self, _id, websocket, retry_index, data) -> None:
        self._id = _id
        self.websocket = websocket
        self.retry_index = retry_index
        self.data = data