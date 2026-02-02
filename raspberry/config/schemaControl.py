"""
Código responsável por controlar o arquivo de
condfigurações dos módulos juntamente com o dataclass 

Deve garantir atomicidade ao editar as variáveis
e arquivos json.
"""

from config.scheme import Configuration
from config.fileControl import update, CONFIGPATH

class SchemaControl:
    def __init__(self, dataclass: Configuration) -> None:
        self.dataclass = dataclass

    def set_max_value(self, module_code:str, new_value: float):
        module = self.dataclass.get_module(module_code)
        if module is not None:
            module.get('levels').update({'max': new_value})
            update(CONFIGPATH, self.dataclass.get_as_dict())

    def set_min_value(self, module_code:str, new_value: float):
        module = self.dataclass.get_module(module_code)
        if module is not None:
            module.get('levels').update({'min': new_value})
            update(CONFIGPATH, self.dataclass.get_as_dict())

    def set_interval(self, module_code:str, new_value: int):
        module = self.dataclass.get_module(module_code)
        if module is not None:
            module.update({'intervals': new_value})
            update(CONFIGPATH, self.dataclass.get_as_dict())