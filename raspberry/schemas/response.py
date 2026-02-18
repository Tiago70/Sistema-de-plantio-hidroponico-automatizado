from dataclasses import dataclass, field

@dataclass(frozen=True)
class Error:
    err_type: str
    cause: str

@dataclass(frozen=True)
class Response:
    ok: bool
    payload: str
    error: Error | None = field(default=None)