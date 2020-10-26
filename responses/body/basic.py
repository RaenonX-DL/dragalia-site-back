"""Basic response body class."""
from abc import ABC

from responses.code import ResponseCode

__all__ = ("Response", "ResponseKey")


class ResponseKey:
    CODE = "code"
    SUCCESS = "success"


class Response(ABC):
    """The most basic request response body."""

    def __init__(self, code: ResponseCode):
        self._code = code

    def serialize(self):
        return {
            ResponseKey.CODE: self._code.code,
            ResponseKey.SUCCESS: self._code.success
        }
