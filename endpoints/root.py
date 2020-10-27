"""Endpoints at the root. Serve as a status checking endpoint."""
from responses import RootTestResponse, ResponseCodeCollection

from .base import EndpointBase

__all__ = ("EPRootTest",)


class EPRootTest(EndpointBase):
    """Endpoint at the root path of the app."""

    def get(self):  # pylint: disable=no-self-use, missing-function-docstring
        return RootTestResponse(ResponseCodeCollection.SUCCESS), 200
