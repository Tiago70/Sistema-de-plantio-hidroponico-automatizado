from dataclasses import dataclass
from typing import Optional

# Melhorar a padronização interna com a externa
# Este código irá causar muita confusão

@dataclass(frozen=True)
class Error:
    err_type: str
    cause: str

@dataclass(frozen=True)
class Response:
    ok: bool
    payload: str
    error: Optional[Error] = None