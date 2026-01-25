"""
Código responsável por tratar qualquer erro que ocorrer
no serial, padronizar o retorno das mensagens recebida
do arduino e garantir a atomicidade do acesso ao Serial. 
"""
from arduinoSerial.ioserial import IoSerial
from threading import Lock
from errors.base import HydroponicsException
from dataclasses import dataclass

@dataclass
class Error:
    type: str
    cause: str

@dataclass
class Response:
    ok: bool
    payload: str
    error: Error | None

class SerialService():
    def __init__(self, serial: IoSerial) -> None:
        self.serial = serial
        self.locking = Lock()

    def get_data(self, module_code: str, action: str | None = '') -> Response:
        with self.locking:
            try:
                message = module_code
                if action:
                    message = message + f' {action}'
                self.serial.send(f'{module_code}\n'.encode('utf-8'))
                data = self.serial.get()
                return Response(ok=True, payload=data, error=None)
            except HydroponicsException as e:
                type = e.__class__.__name__
                message_error = e.__str__()

                return Response(
                    ok=False,
                    payload='An error occurred during serial communication ',
                    error=Error(type=type, cause=message_error)
                )
            