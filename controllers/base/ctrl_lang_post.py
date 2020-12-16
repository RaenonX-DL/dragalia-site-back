"""Multilingual post controller base and its related data structure."""
from abc import ABC
from datetime import datetime
from typing import Any, Optional, Type

import pymongo

from controllers.results import UpdateResult
from .ctrl_lang import MultilingualDataController, MultilingualDataKey, MultilingualGetOneResult

__all__ = ("MultilingualPostController", "MultilingualPostKey")


class MultilingualPostKey(MultilingualDataKey, ABC):
    """Keys for the multilingual posts."""

    VIEW_COUNT: str = "_vc"


class MultilingualPostController(MultilingualDataController):
    """Multilingual post controller."""

    def __init__(self, key_class: Type[MultilingualPostKey]):
        self._view_count_key = key_class.VIEW_COUNT

        super().__init__(key_class)

    def _get_post_list(
            self, lang_code: str, projection: dict[str, int], /,
            start: int = 0, limit: int = 0
    ) -> tuple[list[dict[str, Any]], int]:
        """Get the post list of the controller."""
        return (
            sorted(
                self.find({self._lang_code_key: lang_code},
                          projection=projection,
                          sort=[(self._last_mod_key, pymongo.DESCENDING)])
                    .skip(start)
                    .limit(limit),
                key=lambda item: item[self._last_mod_key],
                reverse=True
            ),
            self.count_documents({self._lang_code_key: lang_code})
        )

    def get_post(self, seq_id: int, lang_code: str = "cht", inc_count: bool = True) -> MultilingualGetOneResult:
        """
        Get a post by its ``seq_id`` and ``lang_code`` with available languages and if it's in an alt language.

        Increases the post view count if ``inc_count`` is ``True``.

        Will not check for the other available languages if the count will not be increased,
        because such condition only happens when fetching the post for edit.
        """
        # Early termination on no sequential ID
        if not seq_id:
            return MultilingualGetOneResult(None, False, [])

        other_langs = []
        if inc_count:
            other_langs = [
                data[self._lang_code_key]
                for data in self.find(
                    {self._seq_id_key: seq_id, self._lang_code_key: {"$ne": lang_code}},
                    projection={self._lang_code_key: 1}
                )
            ]

        post = self.find_one_and_update(
            {self._seq_id_key: seq_id, self._lang_code_key: lang_code},
            {"$inc": {self._view_count_key: 1 if inc_count else 0}}
        )
        in_alt_lang = False

        if not post:
            post = self.find_one_and_update({self._seq_id_key: seq_id}, {"$inc": {self._view_count_key: 1}})
            in_alt_lang = True

        return MultilingualGetOneResult(post, in_alt_lang, other_langs)

    def update_post(self, seq_id: Optional[int], lang_code: str, update_data: dict[str, Any], modify_note: str, /,
                    addl_update_cond: dict[str, Any] = None) -> UpdateResult:
        """
        Update a multilingual post with the key ``(seq_id, lang_code)``.

        Returns ``UpdateResult.NOT_FOUND`` if ``seq_id`` is ``None``.
        This occurs when the sequential was not being passed in via the API endpoints.

        :param seq_id: sequential ID of the post
        :param lang_code: language code of the post
        :param update_data: data to be used to overwrite the data in the database
        :param modify_note: modification note
        :param addl_update_cond: additional update condition
        :return: result of the update
        """
        if not seq_id:
            return UpdateResult.NOT_FOUND

        now = datetime.utcnow()

        update_cond = {
            self._seq_id_key: seq_id,
            self._lang_code_key: lang_code
        }
        if addl_update_cond:
            update_cond |= addl_update_cond

        update_data |= {self._last_mod_key: now}

        update_result = self.update_one(
            update_cond,
            {
                "$set": update_data,
                "$push": {
                    self._mod_notes_key: {
                        self._mod_dt_key: now,
                        self._mod_note_key: modify_note
                    }
                }
            }
        )

        if update_result.matched_count == 0:
            return UpdateResult.NOT_FOUND

        # `NO_CHANGE` is impossible for now since each time a modification note will be pushed
        return UpdateResult.UPDATED if update_result.modified_count > 0 else UpdateResult.NO_CHANGE
