"""Base data controller (a mongodb collection instance)."""
from abc import ABC

from pymongo.collection import Collection, ReturnDocument

from .config import MONGO_CLIENT
from .ctrl_prop import CollectionPropertiesMixin

SEQ_COUNTER = "_seq_counter"
SEQ_NAME = "_col"
SEQ_COUNT = "_seq"


class BaseCollection(CollectionPropertiesMixin, Collection, ABC):
    """Base class for a collection instance."""

    def __init__(self, sequential: bool = False):
        self._db = MONGO_CLIENT.get_database(self.get_db_name())

        super().__init__(self._db, self.get_col_name())

        self.build_indexes()

        self._seq = None
        if sequential:
            self._seq = MONGO_CLIENT \
                .get_database(self.get_db_name()) \
                .get_collection(SEQ_COUNTER)

            self._seq_num = self._seq.find_one_and_update(
                {SEQ_NAME: self.get_col_name()},
                {"$inc": {SEQ_COUNT: 0}},
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )[SEQ_COUNT]

    def get_next_seq_id(self, /, increase: bool = True) -> int:
        """Get the next sequential number. If ``increase`` is ``1``, increase the sequential ID."""
        if self._seq is None:
            raise ValueError("This collection is not sequential.")

        if increase:
            self._seq_num += 1
            self._seq.update_one({SEQ_NAME: self.get_col_name()}, {"$set": {SEQ_COUNT: self._seq_num}})

        return self._seq_num

    def build_indexes(self):
        """Method to be called when building the indexes of this collection."""
