import pytest
from unittest.mock import Mock
from arduinoSerial.ioserial import IoSerial 

@pytest.fixture
def fake_serial_connection():
    """ 
    Mock padrão para os testes que usam o serial
    Utiliza valores corretos
    """
    serial = Mock(name='FakeSerialConnection')
    serial.reset_input_buffer.return_value = None
    serial.write.return_value = None
    serial.readline.return_value = b'1=OK\n'
    serial.close.return_value = None
    serial.open.return_value = None
    serial.is_open = True
    return serial

@pytest.fixture
def fake_ioserial(fake_serial_connection):
    """ Fixture para testes que usam o ioserial """
    return IoSerial(fake_serial_connection)