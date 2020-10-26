"""Enum for the data update result."""
from enum import Enum, auto

__all__ = ("UpdateResult",)


class UpdateResult(Enum):
    """Result of a data update."""

    NOT_FOUND = auto()
    NO_CHANGE = auto()
    UPDATED = auto()
