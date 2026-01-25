import pytest

from arduinoSerial.ioserial import SerialConnection, IoSerial
from errors.communication import (
    ArduinoCommunicationException,
    NoResponseException,
    TimeoutException
    )

class TestSerialConnection:
    def test_constructor_SerialConnection(self):
        connection = SerialConnection('/dev/ttyACM0', 9600, 2)

        assert connection.serial_port == '/dev/ttyACM0'
        assert connection.speed == 9600
        assert connection.timeout == 2

class TestIoSerial:
    def test_constructor_IoSerial(self, fake_serial_connection):
        """ Testa o construtor o IoSerial """
        ioserial = IoSerial(fake_serial_connection)
        assert ioserial.arduino == fake_serial_connection

    def test_validate_response(self, fake_ioserial):
        """
        Testa todos os erros que podem ocorrer ao validar as
        respostas do arduino
        """
        # deve lançar um erro em caso de uma resposta vazia
        with pytest.raises(NoResponseException):
            fake_ioserial._validate_response('')

        # deve lançar um erro caso a resposta não termine com \n
        with pytest.raises(TimeoutException):
            fake_ioserial._validate_response('1>OK')

        # deve lançar um erro caso o código de status enteja com o valor zero
        with pytest.raises(ArduinoCommunicationException):
            fake_ioserial._validate_response('0>Error\n')

    def test_get_response_only(self, fake_ioserial):
        """ Testa o método get para garantir que está retornando apenas a mensagem  """
        # lembrando que o método readline chamado pelo get_response
        # está retornando '1=OK\n' portando deve retornar apenas OK
        assert fake_ioserial.get() == 'OK'

    # método send impossível de testar