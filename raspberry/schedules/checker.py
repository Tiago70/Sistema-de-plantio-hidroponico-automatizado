"""
Código responsável por verificar os dados retornados pelo
serial

Deve lançar avisos ou erros para o notificador caso o valor
dos sensores estejam muito alto, baixo ou se der um erro
na comunicação
"""

from arduinoSerial.service import SerialService
from config.scheme import Configuration
from utils.notifier import NotificationType, Notification, Notifier

class Checker:
    def __init__(self, serial: SerialService, modules: Configuration, notifier: Notifier) -> None:
        self.serial = serial
        self.modules = modules
        self.notifier = notifier

    def run(self, module_code:str, command:str):        
        response = self.serial.execute_command(module_code, command)
        if not response.ok:
            self.notifier.emit(
                Notification(
                    message=f'{response.error.type}:{response.error.cause}',
                    type=NotificationType.ERROR
                    )
                )
            return

        if (module_code == self.modules.temperature.get('code') or
                module_code == self.modules.conductivity.get('code')) :

            self.check_value(module_code, float(response.payload))
    
    def check_value(self, module_code:str, value: float):
        module_to_check = self.modules.get_as_dict()
        
        for module_key in module_to_check.keys():
            if module_code == module_to_check.get(module_key).get('code'):
                module = module_to_check.get(module_key)

                if self.modules.is_high(module_code, value):
                    self.notifier.emit(
                        Notification(
                        message=f'The {module.get('name')} value is high. Value: {value}',
                        type=NotificationType.WARNING
                        )
                    )
                    return

                if self.modules.is_low(module_code, value):
                    self.notifier.emit(
                        Notification(
                        message=f'The {module.get('name')} value is low. Value: {value}',
                        type=NotificationType.WARNING
                        )
                    )