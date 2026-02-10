"""
Código responsável por armazenar, distribuir os
atributos e métodos de verificação dos módulos
"""

from dataclasses import dataclass, fields, asdict
from typing import Any

@dataclass
class Values:
    max: float
    min: float

@dataclass
class Attributes:
    name: str
    code: str
    intervals: list[int]
    levels: Values | None
    actions: dict

@dataclass
class Configuration:
    temperature: Attributes    
    conductivity: Attributes
    water_pump: Attributes
    clock: Attributes

    def get_module(self, module_code: str) -> dict[str, Any] | None:
        for field in fields(self):
            module = getattr(self, field.name)

            if module_code == module.get('code'):
                return module

        return None

    def get_max_value(self, module_code: str) -> float | None:
        module = self.get_module(module_code)
        if module is not None:
            max_value = module.get('levels').get('max')
            if max_value:
                return max_value

        return None

    def get_min_value(self, module_code: str) -> float | None:
        module = self.get_module(module_code)
        if module is not None:
            min_value = module.get('levels').get('min')
            if min_value:
                return min_value

        return None

    def get_as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def is_high(self, module_code: str, value: float) -> bool:
        max_value = self.get_max_value(module_code)
        if max_value:
            return value > max_value

        return False

    def is_low(self, module_code: str, value: float) -> bool:
        min_value = self.get_min_value(module_code)
        if min_value:
            return value < min_value

        return False