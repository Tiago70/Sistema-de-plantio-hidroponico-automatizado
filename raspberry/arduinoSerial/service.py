"""
Código responsável por tratar qualquer erro que ocorrer
no serial, padronizar o retorno das mensagens recebidas
do arduino e garantir a atomicidade do acesso ao Serial. 
"""

from arduinoSerial.ioserial import IoSerial
from threading import Lock
from errors.base import HydroponicsException
from schemas.response import Response, Error
import asyncio

class SerialService():
    def __init__(self, serial: IoSerial) -> None:
        self.serial = serial
        self.locking = Lock()

    def send_command(self, message: str) -> Response:
        with self.locking:
            try:
                self.serial.send(message)
                data = self.serial.get()
                return Response(ok=True, payload=data, error=None)

            except HydroponicsException as e:
                type = e.__class__.__name__
                message_error = e.__str__()

                return Response(
                    ok=False,
                    payload='An error occurred during serial communication ',
                    error=Error(err_type=type, cause=message_error)
                )

    async def execute_command(self, module_code: str, action: str = '') -> Response:
        message = f'{module_code} {action}' if action else module_code

        return await asyncio.to_thread(
            self.send_command,
            message
        )