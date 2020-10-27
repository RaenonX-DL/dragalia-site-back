"""Various errors for the server."""
from abc import ABC

from responses.code import ResponseCodeCollection

from .basic import Response, ResponseKey

__all__ = ("Error404Response", "Error405Response", "Error422Response", "Error500Response")


class ServerErrorResponseKey(ResponseKey):
    MESSAGE = "message"
    EXTRA = "extra"


class ServerErrorResponse(Response, ABC):
    def __init__(self, error, extra: str = ""):
        super().__init__(ResponseCodeCollection.FAILED_SERVER_ERROR)

        self._error = error
        self._extra = extra

    def serialize(self):
        return super().serialize() | {
            ServerErrorResponseKey.MESSAGE: str(self._error),
            ServerErrorResponseKey.EXTRA: self._extra
        }


class Error400Response(ServerErrorResponse):
    def __init__(self, error):
        super().__init__(error)


class Error404Response(ServerErrorResponse):
    def __init__(self, error, extra: str = ""):
        super().__init__(error, extra)


class Error405Response(ServerErrorResponse):
    def __init__(self, error):
        super().__init__(error, "Method not allowed")


class Error422Response(ServerErrorResponse):
    def __init__(self, error):
        super().__init__(error, "Entity unproccessible")


class Error500Response(ServerErrorResponse):
    def __init__(self, error, extra: str = ""):
        super().__init__(error, extra)
