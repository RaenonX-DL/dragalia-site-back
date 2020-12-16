"""Quest post data controllers."""
from datetime import datetime
from typing import Any, Optional

from controllers.base import ModifiableDataKey, MultilingualPostController, MultilingualPostKey
from controllers.results import UpdateResult

__all__ = ("QuestPostKey", "QuestPostController")

DB_NAME = "post"


class QuestPostKey(ModifiableDataKey, MultilingualPostKey):
    """Keys for a single quest post."""

    TITLE = "t"

    # BOSS_CODE = "b" - Not yet implemented

    GENERAL_INFO = "g"
    VIDEO = "v"

    INFO_PARENT = "i"
    INFO_POSITION = "p"
    INFO_BUILDS = "b"
    INFO_ROTATIONS = "r"
    INFO_TIPS = "t"

    ADDENDUM = "a"

    @classmethod
    def is_positional_info_completed(cls, positional_info_single: dict[str, str]) -> bool:
        """Check if ``positional_info_single`` has all the required keys."""
        return positional_info_single.keys() == {cls.INFO_POSITION, cls.INFO_BUILDS, cls.INFO_ROTATIONS, cls.INFO_TIPS}


class _QuestPostController(MultilingualPostController):
    """Quest post data controller."""

    database_name = DB_NAME
    collection_name = "quest"

    def __init__(self):
        super().__init__(QuestPostKey)

    def get_posts(
            self, lang_code: str, /, start: int = 0, limit: int = 0
    ) -> tuple[list[dict[str, Any]], int]:
        """
        Get the posts sorted by the last modified date DESC and the total post count.

        This method only returns key information of posts like sequential id (``s``), title (``t``), last modified
        timestamp (``d_m``) and published timestamp (``d_p``).

        :param lang_code: language code
        :param start: starting index of the result
        :param limit: maximum count of the results to be returned
        :return: list of post records
        """
        projection = {
            QuestPostKey.SEQ_ID: 1,
            QuestPostKey.LANG_CODE: 1,
            QuestPostKey.TITLE: 1,
            QuestPostKey.DT_LAST_MODIFIED: 1,
            QuestPostKey.DT_PUBLISHED: 1,
            QuestPostKey.VIEW_COUNT: 1
        }

        return self._get_post_list(lang_code, projection, start=start, limit=limit)

    def publish_post(
            self, title: str, lang_code: str, general_info: str, video: str,
            position_info: list[dict[str, str]], addendum: str, /, seq_id: Optional[int] = None) -> int:
        """
        Publish a quest post and get its sequential ID.

        Data in ``position_info`` should be insertion-ready (i.e. the keys of each data is already using the key
        from the data model).

        If ``seq_id`` is not specified, a new sequential ID will be used. Otherwise, use the given one.

        :param title: title of the post
        :param lang_code: language code of the post
        :param general_info: general info of the post
        :param video: video of the post
        :param position_info: positional info for each positions in the post
        :param addendum: addendum of the post
        :param seq_id: sequential ID of the post
        :return: sequential ID lf the newly published post
        :raises ValueError: positional info (`position_info`) is incomplete or not using the model key
        """
        new_seq_id = seq_id or self.get_next_seq_id()
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

    def edit_post(
            self, seq_id: int, title: str, lang_code: str, general_info: str, video: str,
            position_info: list[dict[str, str]], addendum: str,
            modify_note: str) -> UpdateResult:
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
        # pylint: disable=too-many-arguments

        return self.update_post(
            seq_id,
            lang_code,
            {
                QuestPostKey.TITLE: title,
                QuestPostKey.GENERAL_INFO: general_info,
                QuestPostKey.VIDEO: video,
                QuestPostKey.INFO_PARENT: position_info,
                QuestPostKey.ADDENDUM: addendum
            },
            modify_note
        )


QuestPostController = _QuestPostController()
