from arduinoSerial.service import SerialService
import pytest

@pytest.fixture
def serialservice(fake_ioserial):
    return SerialService(fake_ioserial)

class TestSerialService:
    def test_contructor(self, fake_ioserial):
        """ Testa o contrutor do SerialService """
        service = SerialService(fake_ioserial)
        assert service.serial == fake_ioserial
        assert service.locking != None

    def test_execute_command_must_return_ok(self, serialservice):
        response = serialservice.execute_command('B')
        assert response.ok == True
        assert response.payload == 'OK'
        assert response.error == None

    def test_execute_command_must_return_an_error(self, fake_ioserial):
        fake_ioserial.arduino.readline.return_value = b'0=Example of an error message\n'
        service = SerialService(fake_ioserial)

        response = service.execute_command('B')
        assert response.ok == False
        assert response.payload == 'An error occurred during serial communication '
        assert response.error.type == 'ArduinoCommunicationException'
        assert response.error.cause == 'Message returned by Arduino: 0=Example of an error message\n'