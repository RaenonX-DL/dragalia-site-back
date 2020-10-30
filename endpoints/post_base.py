"""Base classes for endpoint processing of the post data."""
from abc import ABC
from typing import Any

from webargs import fields

from .base import EPParamBase

__all__ = ("EPPostListParamBase", "EPSinglePostParamBase", "EPPostModifyParamBase")

DEFAULT_LIST_LIMIT = 25


class EPSinglePostParamBase(EPParamBase, ABC):
    """Parameter base class for the request of checking the ID availability."""

    SEQ_ID = "seq_id"
    LANG_CODE = "lang"

    @classmethod
    def base_args(cls) -> dict[str, Any]:
        """Get the base arguments to be used for parse."""
        return super().base_args() | {
            EPSinglePostParamBase.SEQ_ID: fields.Int(missing=None),
            EPSinglePostParamBase.LANG_CODE: fields.Str(missing=None)
        }


class EPPostModifyParamBase(EPSinglePostParamBase, ABC):
    """Parameter base class for the request which modifies a post."""

    MODIFY_NOTE = "modify_note"

    @classmethod
    def base_args(cls) -> dict[str, Any]:
        """Get the base arguments to be used for parse."""
        return super().base_args() | {
            EPPostModifyParamBase.MODIFY_NOTE: fields.Str(),
        }


class EPPostListParamBase(EPParamBase, ABC):
    """Parameter base class for the request of a list of posts."""

    LANG_CODE = "lang_code"
    START = "start"
    LIMIT = "limit"

    @classmethod
    def base_args(cls) -> dict[str, Any]:
        """Get the base arguments to be used for parse."""
        return super().base_args() | {
            EPPostListParamBase.LANG_CODE: fields.Str(),
            EPPostListParamBase.START: fields.Int(default=0),
            EPPostListParamBase.LIMIT: fields.Int(default=DEFAULT_LIST_LIMIT)
        }
