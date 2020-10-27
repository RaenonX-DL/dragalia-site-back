"""Various errors for the server."""
from abc import ABC

from responses.code import ResponseCodeCollection

from .basic import Response, ResponseKey

__all__ = ("Error400Response", "Error404Response", "Error405Response", "Error422Response", "Error500Response")


class ServerErrorResponseKey(ResponseKey):
    """Keys for creating the server error response body."""

    MESSAGE = "message"
    EXTRA = "extra"


class ServerErrorResponse(Response, ABC):
    """Base server error response body."""

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
    """Error response body to be used when 400 error occurred."""


class Error404Response(ServerErrorResponse):
    """Error response body to be used when 404 error occurred."""


class Error405Response(ServerErrorResponse):
    """Error response body to be used when 405 error occurred."""

    def __init__(self, error):
        super().__init__(error, "Method not allowed")


class Error422Response(ServerErrorResponse):
    """Error response body to be used when 422 error occurred."""

    def __init__(self, error):
        super().__init__(error, "Entity unproccessible")


class Error500Response(ServerErrorResponse):
    """Error response body to be used when 500 error occurred."""
