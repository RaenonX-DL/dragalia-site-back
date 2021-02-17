"""Multilingual data controller base and its related data structure."""
from abc import ABC
from dataclasses import dataclass
from typing import Any, Optional, Type, Union

import pymongo

from .ctrl import BaseCollection
from .post_mod import ModifiableDataKey

__all__ = ("MultilingualDataController", "MultilingualGetOneResult", "MultilingualDataKey")


class MultilingualDataKey(ABC):
    """Keys for the multilingual data."""

    SEQ_ID: str = "_seq"
    LANG_CODE: str = "_lang"


@dataclass
class MultilingualGetOneResult:
    """Result object of getting a single multilingual data."""

    data: Optional[dict[str, Any]]  # pylint: disable=unsubscriptable-object
    is_alt_lang: bool
    other_langs: list[str]


class MultilingualDataController(BaseCollection, ABC):  # lgtm [py/missing-equals]
    """Multilingual data controller."""

    def __init__(self, key_class: Type[Union[MultilingualDataKey, ModifiableDataKey]]):
        self._seq_id_key = key_class.SEQ_ID
        self._lang_code_key = key_class.LANG_CODE

        self._last_mod_key = key_class.DT_LAST_MODIFIED

        self._mod_notes_key = key_class.MODIFY_NOTES
        self._mod_note_key = key_class.MODIFY_NOTE
        self._mod_dt_key = key_class.MODIFY_DT

        super().__init__(True)

    def build_indexes(self):
        self.create_index(
            [
                (self._seq_id_key, pymongo.DESCENDING),
                (self._lang_code_key, pymongo.ASCENDING)
            ],
            unique=True
        )

    def is_id_lang_available(self, seq_id: Optional[int], lang_code: str) -> bool:
        """
        Check if the given ID and language code is available.

        :param seq_id: sequential ID to be checked
        :param lang_code: language code to be checked
        :return: if the combination is available
        """
        if not seq_id:
            return True

        if seq_id > self.get_next_seq_id(increase=False):
            return False

        return self.find_one({self._seq_id_key: seq_id, self._lang_code_key: lang_code}) is None
