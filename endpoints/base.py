"""Base classes for an endpoint."""
from flask_restful import Resource
from webargs import fields

__all__ = ("EndpointBase", "EPParamBase")


class EPParamBase:
    """Endpoint parameter base class."""

    GOOGLE_UID = "google_uid"


class EndpointBase(Resource):  # Cannot use `ABC` because of meta class conflict
    """Endpoint base class."""

    @staticmethod
    def base_args():
        """Get the base arguments to be used for parse."""
        return {EPParamBase.GOOGLE_UID: fields.Str(missing=None)}
