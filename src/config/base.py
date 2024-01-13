from uuid import UUID
from typing import Optional

TYPE_KEY = '_type'
ID_KEY = '_id'
DESCRIPTION_KEY = 'description'
DATA_KEY = 'data'



class BaseResponse:
    def __init__(self, t, description, _id=None) -> None:
        self.t = t
        self._id = _id
        self.description = description

    def dump(self):
        return {
            TYPE_KEY: self.t,
            ID_KEY: str(self._id),
            DESCRIPTION_KEY: self.description,
        }
    
class BaseMessageType:
    def __init__(self, t, callback, fixed={}, types={}) -> None:
        self._type = t

        self.fixed = {
            TYPE_KEY: t,
            **fixed
        }

        self.types = {
            TYPE_KEY: str,
            ID_KEY: UUID,
            **types
        }

        self.callback = callback

        for k in self.fixed.keys():
            if (k not in self.types.keys()):
                assert RuntimeError('Required key must be in types key!')

    def convert_package_types(self, package: dict) -> Optional[dict]:
        new_package = {}
        for k, v in package.items():
            if (not k in self.types): return
            try:
                new_package[k] = self.types[k](v)
            except ValueError:
                return
        return new_package

    async def fetch_response(self, *args, **kwargs) -> BaseResponse:
        return await self.callback(*args, **kwargs)

