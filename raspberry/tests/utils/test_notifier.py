from utils.notifier import Notification, NotificationType, Notifier
from pytest import fixture
from unittest.mock import Mock

@fixture
def notf():
    return Notifier()

class TestNotifier:
    def test_constructor(self, notf):
        assert notf.subscribers == []

    def test_subscribe(self, notf):
        """ Testa se o notificador está guardando corretamente as funções """
        def callback_function():
            ...
        notf.subscribe(callback_function)
        assert notf.subscribers[0] == callback_function

    def test_callback(self, notf):
        """ Testa se o notificador está chamando corretamente as funções """
        callback_function1 = Mock()
        callback_function2 = Mock()

        notf.subscribe(callback_function1)
        notf.subscribe(callback_function2)
        
        notf.emit(Notification(message='Test', type=NotificationType.ERROR))
        
        callback_function1.assert_called_once()
        callback_function2.assert_called_once()