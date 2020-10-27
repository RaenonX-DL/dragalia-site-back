"""Response body for getting the data related to quest posts."""
from abc import ABC
from typing import Any

from controllers import QuestPostGetOneResult, QuestPostKey
from responses.code import ResponseCodeCollection

from .basic import Response, ResponseKey

__all__ = ("QuestPostPublishSuccessResponse", "QuestPostPublishFailedResponse", "QuestPostPublishSuccessResponseKey",
           "QuestPostListResponse", "QuestPostListResponseKey",
           "QuestPostGetSuccessResponse", "QuestPostGetFailedResponse", "QuestPostGetSuccessResponseKey",
           "QuestPostEditSuccessResponse", "QuestPostEditFailedResponse", "QuestPostEditSuccessResponseKey",
           "QuestPostIDCheckResponseKey", "QuestPostIDCheckResponse")


# region Quest Post / Update (Base of edit/publish)

class QuestPostUpdateSuccessResponseKey(ResponseKey, ABC):
    """Response keys of successfully published/edited a post."""

    IS_ADMIN = "isAdmin"

    POST_SEQ_ID = "seqId"


class QuestPostUpdateSuccessResponse(Response, ABC):
    """Response body of successfully published/edited a post."""

    def __init__(self, seq_id: int):
        super().__init__(ResponseCodeCollection.SUCCESS)

        self._seq_id = seq_id

    def serialize(self):
        return super().serialize() | {
            QuestPostPublishSuccessResponseKey.POST_SEQ_ID: self._seq_id
        }


class QuestPostUpdateFailedResponse(Response, ABC):
    """Response body of failed to publish/edit a post."""

# endregion


# region Quest Post / Publish

class QuestPostPublishSuccessResponseKey(QuestPostUpdateSuccessResponseKey):
    """Response keys of successfully published a post."""


class QuestPostPublishSuccessResponse(QuestPostUpdateSuccessResponse):
    """Response body of successfully published a post."""


class QuestPostPublishFailedResponse(QuestPostUpdateFailedResponse):
    """Response body of failed to publish a post."""

# endregion


# region Quest Post / List

class QuestPostListResponseKey(ResponseKey):
    """
    Response keys of getting a quest post list.

    Keys must be consistent with the type ``QuestPostListResponse`` at the front side.
    """

    IS_ADMIN = "isAdmin"

    POSTS = "posts"
    START_IDX = "startIdx"
    POST_COUNT = "postCount"

    # These keys need to be consistent with the definition structure at the front side
    # Type name: `PostLintEntry`
    POSTS_SEQ_ID = "seqId"
    POSTS_LANG = "lang"
    POSTS_TITLE = "title"
    POSTS_VIEW_COUNT = "viewCount"
    POSTS_LAST_MODIFIED = "modified"
    POSTS_PUBLISHED = "published"

    @classmethod
    def convert_posts_key(cls, posts: list[dict[str, Any]]):
        """Convert the keys in ``posts`` from model key to be the keys for the response."""
        ret = []

        for post in posts:
            ret.append({
                cls.POSTS_SEQ_ID: post[QuestPostKey.SEQ_ID],
                cls.POSTS_LANG: post[QuestPostKey.LANG_CODE],
                cls.POSTS_TITLE: post[QuestPostKey.TITLE],
                cls.POSTS_VIEW_COUNT: post[QuestPostKey.VIEW_COUNT],
                cls.POSTS_LAST_MODIFIED: post[QuestPostKey.DT_LAST_MODIFIED],
                cls.POSTS_PUBLISHED: post[QuestPostKey.DT_PUBLISHED]
            })

        return ret


class QuestPostListResponse(Response):
    """Response body of getting a quest post list."""

    def __init__(self, is_admin: bool, posts: list[dict[str, Any]], start_idx: int, post_count: int):
        super().__init__(ResponseCodeCollection.SUCCESS)

        self._is_admin = is_admin
        self._start_idx = start_idx
        self._posts = QuestPostListResponseKey.convert_posts_key(posts)
        self._post_count = post_count

    def serialize(self):
        return super().serialize() | {
            QuestPostListResponseKey.POSTS: self._posts,
            QuestPostListResponseKey.START_IDX: self._start_idx,
            QuestPostListResponseKey.POST_COUNT: self._post_count,
            QuestPostListResponseKey.IS_ADMIN: self._is_admin
        }

# endregion


# region Quest Post / Get

class QuestPostGetSuccessResponseKey(ResponseKey):
    """
    Response keys of getting a post.

    Keys must be consistent with the type ``QuestPostGetResponse`` at the front side.
    """

    IS_ADMIN = "isAdmin"

    SEQ_ID = "seqId"
    TITLE = "title"

    LANG_CODE = "lang"

    GENERAL_INFO = "general"
    VIDEO = "video"

    INFO_PARENT = "info"
    INFO_POSITION = "position"
    INFO_BUILDS = "builds"
    INFO_ROTATIONS = "rotations"
    INFO_TIPS = "tips"

    ADDENDUM = "addendum"

    DT_LAST_MODIFIED = "modified"
    DT_PUBLISHED = "published"

    MODIFY_NOTES = "modifyNotes"
    MODIFY_DT = "timestamp"
    MODIFY_NOTE = "note"

    VIEW_COUNT = "viewCount"

    # Other keys not related to post

    IS_ALT_LANG = "isAltLang"
    OTHER_LANGS = "otherLangs"

    @classmethod
    def convert_info_key(cls, pos_info: list[dict[str, Any]]):
        """Convert the keys in ``pos_info`` from model key to be the keys for the response."""
        ret = []

        for post in pos_info:
            ret.append({
                cls.INFO_POSITION: post[QuestPostKey.INFO_POSITION],
                cls.INFO_BUILDS: post[QuestPostKey.INFO_BUILDS],
                cls.INFO_ROTATIONS: post[QuestPostKey.INFO_ROTATIONS],
                cls.INFO_TIPS: post[QuestPostKey.INFO_TIPS]
            })

        return ret

    @classmethod
    def convert_modify_notes_key(cls, modify_notes: list[dict[str, Any]]):
        """Convert the keys in ``modify_notes`` from model key to be the keys for the response."""
        ret = []

        for mod_note in modify_notes:
            ret.append({
                cls.MODIFY_DT: mod_note[QuestPostKey.MODIFY_DT],
                cls.MODIFY_NOTE: mod_note[QuestPostKey.MODIFY_NOTE]
            })

        return ret


class QuestPostGetSuccessResponse(Response):
    """Response body of getting a quest post list."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, is_admin: bool, get_result: QuestPostGetOneResult):
        super().__init__(ResponseCodeCollection.SUCCESS)

        post = get_result.post

        self._is_admin = is_admin
        self._seq_id = post[QuestPostKey.SEQ_ID]
        self._title = post[QuestPostKey.TITLE]
        self._lang_code = post[QuestPostKey.LANG_CODE]
        self._general = post[QuestPostKey.GENERAL_INFO]
        self._video = post[QuestPostKey.VIDEO]
        self._info = QuestPostGetSuccessResponseKey.convert_info_key(post[QuestPostKey.INFO_PARENT])
        self._addendum = post[QuestPostKey.ADDENDUM]
        self._modified = post[QuestPostKey.DT_LAST_MODIFIED]
        self._published = post[QuestPostKey.DT_PUBLISHED]
        self._modify_notes = QuestPostGetSuccessResponseKey.convert_modify_notes_key(post[QuestPostKey.MODIFY_NOTES])
        self._view_count = post[QuestPostKey.VIEW_COUNT]

        self._is_alt_lang = get_result.is_alt_lang
        self._other_langs = get_result.other_langs

    def serialize(self):
        return super().serialize() | {
            QuestPostGetSuccessResponseKey.IS_ADMIN: self._is_admin,
            QuestPostGetSuccessResponseKey.SEQ_ID: self._seq_id,
            QuestPostGetSuccessResponseKey.TITLE: self._title,
            QuestPostGetSuccessResponseKey.LANG_CODE: self._lang_code,
            QuestPostGetSuccessResponseKey.GENERAL_INFO: self._general,
            QuestPostGetSuccessResponseKey.VIDEO: self._video,
            QuestPostGetSuccessResponseKey.INFO_PARENT: self._info,
            QuestPostGetSuccessResponseKey.ADDENDUM: self._addendum,
            QuestPostGetSuccessResponseKey.DT_LAST_MODIFIED: self._modified,
            QuestPostGetSuccessResponseKey.DT_PUBLISHED: self._published,
            QuestPostGetSuccessResponseKey.MODIFY_NOTES: self._modify_notes,
            QuestPostGetSuccessResponseKey.VIEW_COUNT: self._view_count,
            QuestPostGetSuccessResponseKey.IS_ALT_LANG: self._is_alt_lang,
            QuestPostGetSuccessResponseKey.OTHER_LANGS: self._other_langs
        }


class QuestPostGetFailedResponse(Response):
    """Response body of failing to get a post."""

# endregion


# region Quest Post / Edit

class QuestPostEditSuccessResponseKey(QuestPostUpdateSuccessResponseKey):
    """Response keys of successfully edited a post."""


class QuestPostEditSuccessResponse(QuestPostUpdateSuccessResponse):
    """Response body of successfully edited a post."""


class QuestPostEditFailedResponse(QuestPostUpdateFailedResponse):
    """Response body of failed to edit a post."""

# endregion


# region Quest Post / ID Check

class QuestPostIDCheckResponseKey(ResponseKey):
    """Response keys of a quest post ID check request."""

    IS_ADMIN = "isAdmin"
    AVAILABLE = "available"


class QuestPostIDCheckResponse(Response):
    """Response body of a quest post ID check request."""

    def __init__(self, is_admin: bool, available: bool):
        super().__init__(ResponseCodeCollection.SUCCESS if is_admin else ResponseCodeCollection.FAILED_CHECK_NOT_ADMIN)

        self._is_admin = is_admin
        self._available = available

    def serialize(self):
        return super().serialize() | {
            QuestPostIDCheckResponseKey.IS_ADMIN: self._is_admin,
            QuestPostIDCheckResponseKey.AVAILABLE: self._available,
        }

# endregion
