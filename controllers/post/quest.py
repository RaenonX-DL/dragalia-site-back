"""Quest Post data controllers."""
from datetime import datetime
from typing import Any, Optional

import pymongo

from controllers.base import BaseCollection
from controllers.results import UpdateResult

__all__ = ("QuestPostKey", "QuestPostController")

DB_NAME = "post"


class QuestPostKey:
    """Keys for a single quest post."""

    SEQ_ID = "s"
    TITLE = "t"

    LANG_CODE = "l"

    # BOSS_CODE = "b" - Not yet implemented

    GENERAL_INFO = "g"
    VIDEO = "v"

    INFO_PARENT = "i"
    INFO_POSITION = "p"
    INFO_BUILDS = "b"
    INFO_ROTATIONS = "r"
    INFO_TIPS = "t"
    INFO_POSITION_COMP = f"{INFO_PARENT}.{INFO_POSITION}"
    INFO_BUILDS_COMP = f"{INFO_PARENT}.{INFO_BUILDS}"
    INFO_ROTATIONS_COMP = f"{INFO_PARENT}.{INFO_ROTATIONS}"
    INFO_TIPS_COMP = f"{INFO_PARENT}.{INFO_TIPS}"

    ADDENDUM = "a"

    DT_LAST_MODIFIED = "d_m"
    DT_PUBLISHED = "d_p"

    MODIFY_NOTES = "m_n"
    MODIFY_DT = "dt"
    MODIFY_NOTE = "n"
    MODIFY_DT_COMP = f"{MODIFY_NOTES}.{MODIFY_DT}"
    MODIFY_NOTE_COMP = f"{MODIFY_NOTES}.{MODIFY_NOTE}"

    VIEW_COUNT = "c"

    @classmethod
    def is_positional_info_completed(cls, positional_info_single: dict[str, str]) -> bool:
        return positional_info_single.keys() == {cls.INFO_POSITION, cls.INFO_BUILDS, cls.INFO_ROTATIONS, cls.INFO_TIPS}


class _QuestPostController(BaseCollection):
    """Quest post data controller."""

    database_name = DB_NAME
    collection_name = "quest"

    def __init__(self):
        super().__init__(True)

    def build_indexes(self):
        self.create_index(
            [
                (QuestPostKey.SEQ_ID, pymongo.DESCENDING),
                (QuestPostKey.LANG_CODE, pymongo.ASCENDING)
            ],
            unique=True
        )

    def get_post(self, seq_id: int, lang_code: str = "cht", inc_count: bool = True) -> Optional[dict[str, Any]]:
        """
        Get a post by its ``seq_id`` in ``lang_code``, if provided.

        If the above condition returns nothing, but there's a post with the same ``seq_id``, return it.

        Otherwise, return ``None``.

        Increases the post view count if ``inc_count`` is ``True``.
        """
        ret = self.find_one_and_update(
            {QuestPostKey.SEQ_ID: seq_id, QuestPostKey.LANG_CODE: lang_code},
            {"$inc": {QuestPostKey.VIEW_COUNT: 1 if inc_count else 0}}
        )
        if ret:
            return ret

        return self.find_one_and_update({QuestPostKey.SEQ_ID: seq_id}, {"$inc": {QuestPostKey.VIEW_COUNT: 1}})

    def get_posts(self, /, start: int = 0, limit: int = 0) -> list[dict[str, Any]]:
        """
        Get the posts sorted by the last modified date DESC.

        This method only returns key information of posts like sequential id (``s``), title (``t``), last modified
        timestamp (``d_m``) and published timestamp (``d_p``).

        :param start: starting index of the result
        :param limit: maximum count of the results to be returned
        :return: list of post records
        """
        # TODO: Filter by language code
        projection = {
            QuestPostKey.SEQ_ID: 1,
            QuestPostKey.LANG_CODE: 1,
            QuestPostKey.TITLE: 1,
            QuestPostKey.DT_LAST_MODIFIED: 1,
            QuestPostKey.DT_PUBLISHED: 1,
            QuestPostKey.VIEW_COUNT: 1
        }

        return sorted(
            self.find(projection=projection, sort=[(QuestPostKey.DT_LAST_MODIFIED, pymongo.ASCENDING)])
                .skip(start)
                .limit(limit),
            key=lambda item: item[QuestPostKey.DT_LAST_MODIFIED],
            reverse=True
        )

    def publish_post(self, title: str, lang_code: str, general_info: str, video: str,
                     position_info: list[dict[str, str]], addendum: str) -> int:
        """
        Publish a quest post and get its sequential ID.

        Data in ``position_info`` should be insertion-ready (i.e. the key of each data is already using the key
        from the data model).

        :param title: title of the post
        :param lang_code: language code of the post
        :param general_info: general info of the post
        :param video: video of the post
        :param position_info: positional info for each positions in the post
        :param addendum: addendum of the post
        :return: sequential ID for the newly published post
        :raises ValueError: positional info (`position_info`) is incomplete or not using the model key
        """
        new_seq_id = self.get_next_seq_id()
        now = datetime.utcnow()

        if any(not QuestPostKey.is_positional_info_completed(info) for info in position_info):
            raise ValueError("Incomplete positional info")

        self.insert_one({
            QuestPostKey.SEQ_ID: new_seq_id,
            QuestPostKey.TITLE: title,
            QuestPostKey.LANG_CODE: lang_code,
            QuestPostKey.DT_LAST_MODIFIED: now,
            QuestPostKey.DT_PUBLISHED: now,
            QuestPostKey.GENERAL_INFO: general_info,
            QuestPostKey.VIDEO: video,
            QuestPostKey.INFO_PARENT: position_info,
            QuestPostKey.ADDENDUM: addendum,
            QuestPostKey.MODIFY_NOTES: [],
            QuestPostKey.VIEW_COUNT: 0
        })

        return new_seq_id

    def edit_post(self, seq_id: int, title: str, lang_code: str, general_info: str, video: str,
                  position_info: list[dict[str, str]], addendum: str, modify_note: str) -> UpdateResult:
        """
        Edit a quest post.

        Data in ``position_info`` should be insertion-ready (i.e. the key of each data is already using the key
        from the data model).

        :param seq_id: sequential ID of the post
        :param title: title of the post
        :param lang_code: language code of the post
        :param general_info: general info of the post
        :param video: video of the post
        :param position_info: positional info for each positions in the post
        :param addendum: addendum of the post
        :param modify_note: modification note
        :return: result of the update
        :raises ValueError: positional info (`position_info`) is incomplete or not using the model key
        """
        now = datetime.utcnow()

        if any(not QuestPostKey.is_positional_info_completed(info) for info in position_info):
            raise ValueError("Incomplete positional info")

        update_result = self.update_one(
            {
                QuestPostKey.SEQ_ID: seq_id,
                QuestPostKey.LANG_CODE: lang_code
            },
            {
                "$set": {
                    QuestPostKey.TITLE: title,
                    QuestPostKey.GENERAL_INFO: general_info,
                    QuestPostKey.VIDEO: video,
                    QuestPostKey.INFO_PARENT: position_info,
                    QuestPostKey.ADDENDUM: addendum
                },
                "$push": {
                    QuestPostKey.MODIFY_NOTES: {
                        QuestPostKey.MODIFY_DT: now,
                        QuestPostKey.MODIFY_NOTE: modify_note
                    }
                }
            }
        )

        if update_result.matched_count == 0:
            return UpdateResult.NOT_FOUND

        # `NO_CHANGE` is impossible for now since each time a modification note will be pushed
        return UpdateResult.UPDATED if update_result.modified_count > 0 else UpdateResult.NO_CHANGE

    # DRAFT: Data caching


QuestPostController = _QuestPostController()
