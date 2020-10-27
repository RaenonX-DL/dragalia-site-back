"""Basic response body class."""
from abc import ABC

from responses.code import ResponseCode

__all__ = ("Response", "ResponseKey")


class ResponseKey:
    """Keys to be used in every response body."""

    CODE = "code"
    SUCCESS = "success"


class Response(ABC):
    """The most basic request response body."""

    def __init__(self, code: ResponseCode):
        """Create a response body with ``code`` indicating the result."""
        self._code = code

    def serialize(self):
        """Serialize the response and return it."""
        return {
            ResponseKey.CODE: self._code.code,
            ResponseKey.SUCCESS: self._code.success
        }
