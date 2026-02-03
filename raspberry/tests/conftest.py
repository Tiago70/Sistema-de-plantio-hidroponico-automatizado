import pytest
from unittest.mock import Mock
from arduinoSerial.ioserial import IoSerial
from config.schemaControl import Configuration

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

@pytest.fixture
def fake_dataclass():
    """ Fixture para o dataclass dos módulos """
    test_data = {
        "temperature": {
            "name": "temperature",
            "code": "T",
            "intervals": 1000,
            "levels": {
                "max": 30,
                "min": 10
            },
            "actions": {
                "get_value": ""
            }
        },
        "conductivity": {
            "name": "conductivity",
            "code": "C",
            "intervals": 500,
            "levels": {
                "max": 2,
                "min": 0.1
            },
            "actions": {
                "get_value": ""
            }
        },
        "water_pump": {
            "name": "water_pump",
            "code": "B",
            "intervals": 250,
            "actions": {
                "get_value": "",
                "on": "1",
                "off": 0
            }
        },
        "clock": {
            "name": "clock",
            "code": "R",
            "actions": {
                "get_value": ""
            }
        }
        }

    return Configuration(**test_data)