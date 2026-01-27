"""
Código responsável por cuidar de todas as
notificações do sistema atravez de callbacks
"""

from typing import Callable
from dataclasses import dataclass
from enum import Enum

class NotificationType(Enum):
    ERROR = 'error'
    WARNING = 'warning'

@dataclass(frozen=True)
class Notification:
    message: str
    type: NotificationType
    # adicionar a data e a hora do ocorrido se necessário

class Notifier:
    def __init__(self) -> None:
        self.subscribers: list[Callable[[Notification], None]] = []

    def emit(self, notification: Notification):
        """ Emiti uma notificação para todos os inscritos """
        for subscriber in self.subscribers:
            subscriber(notification)

    def subscribe(self, callback: Callable[[Notification], None]) -> None:
        """ Adiciona uma função para receber notificações quando ocorrer """
        self.subscribers.append(callback)