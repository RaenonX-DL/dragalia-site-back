"""Base key class for modifiable data."""

__all__ = ("ModifiableDataKey",)

from abc import ABC


class ModifiableDataKey(ABC):
    """Base key calss for the modifiable data."""

    DT_PUBLISHED: str = "_dt_pub"
    DT_LAST_MODIFIED: str = "_dt_mod"

    MODIFY_NOTES: str = "_dt_mn"
    MODIFY_DT: str = "dt"
    MODIFY_NOTE: str = "n"
