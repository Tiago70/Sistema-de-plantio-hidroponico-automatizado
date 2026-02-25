from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

class RequestType(IntEnum):
    GET_VALUE = 1

    SET_INTERVAL = 2
    SET_MIN_MAX_VALUE = 3

@dataclass()
class MqttRequest:
    """ Dados padrão para qualquer requisição """
    type: int

@dataclass
class GetDataRequest(MqttRequest):
    target: list[str]

@dataclass
class UpdateIntervalRequest(MqttRequest):
    module: str
    target: str
    value: list[int]

@dataclass
class UpdateMinMaxValueRequest(MqttRequest):
    target: str
    min: Optional[float] = None
    max: Optional[float] = None

    def __post_init__(self):
        if self.min is None and self.max is None:
            raise ValueError(
                "At least one of the min or max values ​​must be provided."
            )

COMMAND_MAP = {
    RequestType.GET_VALUE: GetDataRequest,
    RequestType.SET_INTERVAL: UpdateIntervalRequest,
    RequestType.SET_MIN_MAX_VALUE: UpdateMinMaxValueRequest
}