"""
Código responsável por editar os arquivos json

Deve garantir atomicidade e integridade ao editar
o arquivo
"""

import json
from threading import Lock
from typing import Any
from pathlib import Path
import os

_locking = Lock()
CONFIGPATH = Path(__file__).resolve().parent / 'moduleConfig.json'

def update(file: str, data: Any) -> None:
    file_path = Path(file)
    temp_path = file_path.with_suffix('.tmp')
    with _locking:
        with temp_path.open('w') as f:
            json.dump(data, f, indent=4)
        os.replace(temp_path, file_path)

def read(file: str) -> Any:
    file_path = Path(file)
    with _locking:
        with file_path.open('r') as f:
            return json.load(f)