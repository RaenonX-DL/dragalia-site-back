"""JSON serializer for the response body."""
from datetime import datetime
from json import JSONEncoder

from .body import Response
from .code import ResponseCode

__all__ = ("ResponseBodyEncoder",)


class ResponseBodyEncoder(JSONEncoder):
    """JSON encoder for the response body."""

    def default(self, obj):
        # pylint: disable=arguments-differ
        if isinstance(obj, Response):
            return obj.serialize()
        if isinstance(obj, ResponseCode):
            return obj.code
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S (UTC)")

        return super().default(obj)
