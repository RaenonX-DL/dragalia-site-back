"""Base data controller (a mongodb collection instance)."""
from abc import ABC

from pymongo.collection import Collection

from .config import MONGO_CLIENT
from .ctrl_prop import CollectionPropertiesMixin


class BaseCollection(CollectionPropertiesMixin, Collection, ABC):
    """Base class for a collection instance."""

    def __init__(self, sequential: bool = False):
        self._db = MONGO_CLIENT.get_database(self.get_db_name())

        super().__init__(self._db, self.get_col_name())

        self.build_indexes()

        self._seq = None
        if sequential:
            self._seq = self.count_documents({})

    def get_next_seq_id(self, /, increase: bool = True) -> int:
        """Get the next sequential number. If ``increase`` is ``1``, increase the sequential ID."""
        if self._seq is None:
            raise ValueError("This collection is not sequential.")

        if increase:
            self._seq += 1

        return self._seq

    def build_indexes(self):
        """Method to be called when building the indexes of this collection."""
