from arduinoSerial.service import SerialService
from unittest.mock import patch, AsyncMock
from schemas.response import Response
import pytest

@pytest.fixture
def fake_serialservice(fake_ioserial):
    return SerialService(fake_ioserial)

class TestSerialService:
    def test_contructor(self, fake_ioserial):
        """ Testa o contrutor do SerialService """
        service = SerialService(fake_ioserial)
        assert service.serial == fake_ioserial
        assert service.locking != None

    def test_send_command_must_return_ok(self, fake_serialservice):
        response = fake_serialservice.send_command('B')
        assert response.ok == True
        assert response.payload == 'OK'
        assert response.error == None

    def test_send_command_must_return_an_error(self, fake_ioserial):
        fake_ioserial.arduino.readline.return_value = b'0=Example of an error message\n'
        service = SerialService(fake_ioserial)

        response = service.send_command('B')
        assert response.ok == False
        assert response.payload == 'An error occurred during serial communication '
        assert response.error.err_type == 'ArduinoCommunicationException'
        assert response.error.cause == 'Message returned by Arduino: 0=Example of an error message\n'

    @pytest.mark.asyncio
    async def test_execute_command(self, fake_serialservice):
        with patch("asyncio.to_thread", new_callable=AsyncMock) as mock_to_thread:
            response = Response(ok=True, payload='OK', error=None)
            mock_to_thread.return_value = response

            result = await fake_serialservice.execute_command('B', '1')

            mock_to_thread.assert_called_once_with(
                fake_serialservice.send_command,
                'B 1'
            )
            assert result == response

            await fake_serialservice.execute_command('T')

            mock_to_thread.assert_called_with(
                fake_serialservice.send_command,
                'T'
            )