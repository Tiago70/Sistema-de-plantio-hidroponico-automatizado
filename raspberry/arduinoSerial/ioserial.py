"""
Código responsável por controlar o fluxo de comunicação
serial entre o raspberry e o arduino.

Deve garantir que a integridade da mensagem recebida.

Deve lançar erros quando não for possível a comunicação
ou quando a mensagem recebida estiver com problemas
"""

import serial
import time
from typing import Protocol
from threading import Lock
from errors.communication import (
    ArduinoCommunicationException,
    NoResponseException,
    TimeoutException
    )

class SerialPort(Protocol):
    """ Interface para utilizar Mock """
    def readline(self) -> bytes: ...
    def write(self, data: bytes) -> None: ...
    def reset_input_buffer(self) -> None: ...
    def open(self) -> None: ...
    def close(self) -> None: ...
    is_open: bool

class SerialConnection():
    def __init__(self, serial_port: str, speed: int, timeout: int) -> None:
        self.serial_port = serial_port
        self.speed = speed
        self.timeout = timeout

    def connect(self) -> serial.Serial:
        connection = serial.Serial(
            self.serial_port,
            self.speed,
            timeout=self.timeout)
        time.sleep(2)
        return connection

class IoSerial:
    def __init__(self, connection: SerialPort):
        self.arduino = connection

    def _reconnect(self) -> bool:
        try:
            if self.arduino.is_open:
                self.arduino.close()
            self.arduino.open()
            time.sleep(2)
        except serial.SerialException:
            return False
        else:
            return True

    def _validate_response(self, response: str) -> None:
        if not response:
            raise NoResponseException("No response from the Arduino")
        if not response.endswith('\n'):
            raise TimeoutException("Time expired or incomplete response")

        if response[0] != '1':
            raise ArduinoCommunicationException(f"Message returned by Arduino: {response}")

    def get(self) -> str:
        try:
            arduino_response = self.arduino.readline().decode('utf-8')
        except serial.SerialException:
            if self._reconnect():
                arduino_response = self.arduino.readline().decode('utf-8')
            else:
                raise ArduinoCommunicationException("Without connection to the Arduino")

        self._validate_response(arduino_response)
        # se tudo ocorrer bem separa o código de status da mensagem e retorna a mensagem
        message = arduino_response.split('=')[1]
        return message.replace('\n', '')

    def send(self, message: bytes):
        try:
            self.arduino.reset_input_buffer()
            self.arduino.write(message)
        except serial.SerialException as e:
            if not self._reconnect():
                raise ArduinoCommunicationException("Without connection to the Arduino")
            self.arduino.write(message)