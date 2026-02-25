import json
from arduinoSerial import SerialService
from config.schemaControl import SchemaControl
from schedules.schedule import Schedule
from schemas.response import Response
from schemas.request import (
    GetDataRequest, 
    UpdateIntervalRequest,
    UpdateMinMaxValueRequest
)

class GetDataHandle:
    def __init__(self, serial: SerialService) -> None:
        self.serial = serial

    async def handle(self, req: GetDataRequest) -> Response:
        data = {}
        for module in req.target:
            res = await self.serial.execute_command(module)

            if not res.ok:
                return res
            
            data[module] = res.payload

        return Response(ok=True, payload=json.dumps(data))

# Possivel criação de um event bus, para diminuir esse tanto de dependências
class UpdateIntervalHandle:
    def __init__(self, schedule: Schedule, schema: SchemaControl) -> None:
        self.schedule = schedule
        self.schema = schema

    async def handle(self, req: UpdateIntervalRequest) -> Response:
        self.schema.set_interval(req.module, req.value)
        self.schedule.update_job_interval()

class UpdateMinMaxValueHandle:
    def __init__(self, schema: SchemaControl) -> None:
        pass