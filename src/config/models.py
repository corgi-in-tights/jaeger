class Actor:
    def __init__(self, _id, server, **kwargs) -> None:
        self._id = _id
        self.server = server
        self.data = kwargs

class Message:
    def __init__(self, _id, _type, **kwargs) -> None:
        self._id = _id
        self._type = _type
        self.data = kwargs
    


TYPE_KEY = 'type'
ID_KEY = 'id'
DESCRIPTION_KEY = 'description'
STATUS_KEY = 'status'