from unittest.mock import Mock, AsyncMock
from schedules.checker import Checker
import pytest
from arduinoSerial.service import Response, Error

@pytest.fixture
def fake_checker(fake_dataclass):
    notf = Mock()
    serials = AsyncMock()
    serials.execute_command.return_value = Response(
        ok=1,
        payload='OK',
        error=None
    )
    return Checker(serials, fake_dataclass, notf)

class TestChecker:
    def test_contructor(self, fake_serialservice, fake_dataclass):
        notf = Mock()
        checker = Checker(fake_serialservice, fake_dataclass, notf)

        assert checker.serial == fake_serialservice
        assert checker.modules == fake_dataclass
        assert checker.notifier == notf

    def test_checker(self, fake_checker):
        """
        Testa se o verificador está notificando apenas quando o valor
        lido dos sensores está acima ou abaixo do limite
        """
        # deve chamar uma vez
        fake_checker.check_value('T', 31)
        fake_checker.notifier.emit.assert_called_once()

        # deve chamar de novo. Total de 2
        fake_checker.check_value('T', 9)
        assert fake_checker.notifier.emit.call_count == 2

        # não deve chamar. Total de 2
        fake_checker.check_value('T', 22)
        assert fake_checker.notifier.emit.call_count == 2

        # deve chamar. Total de 3
        fake_checker.check_value('C', 3)
        assert fake_checker.notifier.emit.call_count == 3

        # deve chamar. Total de 4
        fake_checker.check_value('C', 0.09)
        assert fake_checker.notifier.emit.call_count == 4

        # não deve chamar. Total de 4
        fake_checker.check_value('C', 1)
        assert fake_checker.notifier.emit.call_count == 4

    @pytest.mark.asyncio
    async def test_run(self, fake_checker):
        """
        Testa se a função de executar um comando está notificando
        apenas quando ocorrer um erro na leitura

        Também testa se está chamando o checker quando o código do
        módulo for de um sensor
        """

        # mock para a função de checar valor para verificar as chamadas
        fake_checker.check_value = Mock()

        # não deve chamar o método de checar valor em respostas
        # que não sejam números
        await fake_checker.run('B', '1')
        fake_checker.check_value.assert_not_called()

        await fake_checker.run('R', '1')
        fake_checker.check_value.assert_not_called()

        # colocando um valor numérico de retorno
        fake_checker.serial.execute_command.return_value = Response(
            ok=1,
            payload='5.3',
            error=None
        )

        # deve chamar o método de verificação em valores
        # que sejam numéricos
        await fake_checker.run('C', '')
        fake_checker.check_value.assert_called_once()

        await fake_checker.run('T', '')
        assert fake_checker.check_value.call_count == 2

        # também não deve notificar nenhum erro (está retornando OK)
        fake_checker.notifier.emit.assert_not_called()

        # alterando a resposta para retornar um erro
        fake_checker.serial.execute_command.return_value = Response(
            ok=0,
            payload='Error message',
            error=Error(err_type='', cause='')
        )

        # deve chamar o notificador quando ocorrer um erro
        await fake_checker.run('B', '1')
        fake_checker.notifier.emit.assert_called_once()