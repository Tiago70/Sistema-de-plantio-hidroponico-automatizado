from schemas.response import Response

class RequestDispatcher:
    def __init__(self):
        self.handlers = {}

    def register(self, request_type, handler):
        self.handlers[request_type] = handler

    async def dispatch(self, req) -> Response:
        handler = self.handlers[type(req)]
        return await handler.handle(req)