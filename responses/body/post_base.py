"""Base response class related to post data control."""
from abc import ABC
from typing import Any

from controllers import ModifiableDataKey, MultilingualGetOneResult, MultilingualPostKey
from responses.code import ResponseCodeCollection
from .basic import Response, ResponseKey

__all__ = ("PostPublishSuccessResponse", "PostPublishFailedResponse", "PostPublishSuccessResponseKey",
           "PostListResponse", "PostListResponseKey",
           "PostGetSuccessResponse", "PostGetFailedResponse", "PostGetSuccessResponseKey",
           "PostEditSuccessResponse", "PostEditFailedResponse", "PostEditSuccessResponseKey",
           "PostIDCheckResponseKey", "PostIDCheckResponse")


# region Post / Update (Base of edit/publish)

class PostUpdateSuccessResponseKey(ResponseKey, ABC):
    """Response keys of successfully published/edited a post."""

    POST_SEQ_ID = "seqId"


class PostUpdateSuccessResponse(Response, ABC):
    """Response body of successfully published/edited a post."""

    def __init__(self, seq_id: int):
        super().__init__(ResponseCodeCollection.SUCCESS)

        self._seq_id = seq_id

    def serialize(self):
        return super().serialize() | {
            PostUpdateSuccessResponseKey.POST_SEQ_ID: self._seq_id
        }


class PostUpdateFailedResponse(Response, ABC):
    """Response body of failed to publish/edit a post."""


# endregion


# region Post / Publish

class PostPublishSuccessResponseKey(PostUpdateSuccessResponseKey, ABC):
    """Response keys of successfully published a post."""


class PostPublishSuccessResponse(PostUpdateSuccessResponse, ABC):
    """Response body of successfully published a post."""


class PostPublishFailedResponse(PostUpdateFailedResponse, ABC):
    """Response body of failed to publish a post."""


# endregion


# region Post / List

class PostListResponseKey(ResponseKey, ABC):
    """
    Response keys of getting a post list.

    Keys must be consistent with the type ``PostListResponse`` at the front side.
    """

    IS_ADMIN = "isAdmin"
    SHOW_ADS = "showAds"

    POSTS = "posts"
    START_IDX = "startIdx"
    POST_COUNT = "postCount"


class PostListResponse(Response, ABC):
    """Response body of getting a post list."""

    def __init__(self, is_admin: bool, show_ads: bool, start_idx: int, post_count: int):
        super().__init__(ResponseCodeCollection.SUCCESS)

        self._is_admin = is_admin
        self._show_ads = show_ads
        self._start_idx = start_idx
        self._post_count = post_count

    def serialize(self):
        return super().serialize() | {
            PostListResponseKey.START_IDX: self._start_idx,
            PostListResponseKey.POST_COUNT: self._post_count,
            PostListResponseKey.IS_ADMIN: self._is_admin,
            PostListResponseKey.SHOW_ADS: self._show_ads
        }


# endregion


# region Post / Get

class PostGetSuccessResponseKey(ResponseKey, ABC):
    """
    Response keys of getting a multilingual modifiable post.

    Keys must be consistent with the type ``PostGetResponse`` at the front side.
    """

    IS_ADMIN = "isAdmin"
    SHOW_ADS = "showAds"

    SEQ_ID = "seqId"
    LANG_CODE = "lang"

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
    def convert_modify_notes_key(cls, modify_notes: list[dict[str, Any]]):
        """Convert the keys in ``modify_notes`` from model key to be the keys for the response."""
        ret = []

        for mod_note in modify_notes:
            ret.append({
                cls.MODIFY_DT: mod_note[ModifiableDataKey.MODIFY_DT],
                cls.MODIFY_NOTE: mod_note[ModifiableDataKey.MODIFY_NOTE]
            })

        return ret


class PostGetSuccessResponse(Response):
    """Response body of getting a multilingual modifiable post."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, is_admin: bool, show_ads: bool, get_result: MultilingualGetOneResult):
        super().__init__(ResponseCodeCollection.SUCCESS)

        post = get_result.data

        self._is_admin = is_admin
        self._show_ads = show_ads
        self._seq_id = post[MultilingualPostKey.SEQ_ID]
        self._lang_code = post[MultilingualPostKey.LANG_CODE]
        self._modified = post[ModifiableDataKey.DT_LAST_MODIFIED]
        self._published = post[ModifiableDataKey.DT_PUBLISHED]
        self._modify_notes = PostGetSuccessResponseKey.convert_modify_notes_key(post[ModifiableDataKey.MODIFY_NOTES])
        self._view_count = post[MultilingualPostKey.VIEW_COUNT]

        self._is_alt_lang = get_result.is_alt_lang
        self._other_langs = get_result.other_langs

    def serialize(self):
        return super().serialize() | {
            PostGetSuccessResponseKey.IS_ADMIN: self._is_admin,
            PostGetSuccessResponseKey.SHOW_ADS: self._show_ads,
            PostGetSuccessResponseKey.SEQ_ID: self._seq_id,
            PostGetSuccessResponseKey.LANG_CODE: self._lang_code,
            PostGetSuccessResponseKey.DT_LAST_MODIFIED: self._modified,
            PostGetSuccessResponseKey.DT_PUBLISHED: self._published,
            PostGetSuccessResponseKey.MODIFY_NOTES: self._modify_notes,
            PostGetSuccessResponseKey.VIEW_COUNT: self._view_count,
            PostGetSuccessResponseKey.IS_ALT_LANG: self._is_alt_lang,
            PostGetSuccessResponseKey.OTHER_LANGS: self._other_langs
        }


class PostGetFailedResponse(Response):
    """Response body of failing to get a post."""


# endregion


# region Post / Edit

class PostEditSuccessResponseKey(PostUpdateSuccessResponseKey):
    """Response keys of successfully edited a post."""


class PostEditSuccessResponse(PostUpdateSuccessResponse):
    """Response body of successfully edited a post."""


class PostEditFailedResponse(PostUpdateFailedResponse):
    """Response body of failed to edit a post."""


# endregion


# region Quest Post / ID Check

class PostIDCheckResponseKey(ResponseKey):
    """Response keys of a post ID check request."""

    IS_ADMIN = "isAdmin"
    AVAILABLE = "available"


class PostIDCheckResponse(Response):
    """Response body of a post ID check request."""

    def __init__(self, is_admin: bool, available: bool):
        super().__init__(ResponseCodeCollection.SUCCESS if is_admin else ResponseCodeCollection.FAILED_CHECK_NOT_ADMIN)

        self._is_admin = is_admin
        self._available = available

    def serialize(self):
        return super().serialize() | {
            PostIDCheckResponseKey.IS_ADMIN: self._is_admin,
            PostIDCheckResponseKey.AVAILABLE: self._available,
        }

# endregion
