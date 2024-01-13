from websockets import WebSocketServerProtocol
from config.base import TYPE_KEY, ID_KEY, BaseMessageType, BaseResponse
import json
from typing import Optional


async def send_response(websocket: WebSocketServerProtocol, response: BaseResponse):
	await websocket.send(json.dumps(response.dump()))

def has_type_and_id(package: dict) -> bool:
	return TYPE_KEY in package and ID_KEY in package


def convert_package_types(package: dict, message_type: BaseMessageType) -> Optional[dict]:
	if (message_type._type == package[TYPE_KEY]):
		if (package.keys() == message_type.types.keys()):
			return message_type.convert_package_types(package)
	return





