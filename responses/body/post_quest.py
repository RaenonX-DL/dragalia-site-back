"""Response body for getting the data related to quest posts."""
from typing import Any

from controllers import MultilingualGetOneResult, QuestPostKey
from .post_base import (
    PostEditFailedResponse, PostEditSuccessResponse, PostEditSuccessResponseKey, PostGetFailedResponse,
    PostGetSuccessResponse, PostGetSuccessResponseKey, PostIDCheckResponse, PostIDCheckResponseKey, PostListResponse,
    PostListResponseKey, PostPublishFailedResponse, PostPublishSuccessResponse, PostPublishSuccessResponseKey,
)

__all__ = ("QuestPostPublishSuccessResponse", "QuestPostPublishFailedResponse", "QuestPostPublishSuccessResponseKey",
           "QuestPostListResponse", "QuestPostListResponseKey",
           "QuestPostGetSuccessResponse", "QuestPostGetFailedResponse", "QuestPostGetSuccessResponseKey",
           "QuestPostEditSuccessResponse", "QuestPostEditFailedResponse", "QuestPostEditSuccessResponseKey",
           "QuestPostIDCheckResponseKey", "QuestPostIDCheckResponse")


# region Quest Post / Publish

class QuestPostPublishSuccessResponseKey(PostPublishSuccessResponseKey):
    """Response keys of successfully published a quest post."""


class QuestPostPublishSuccessResponse(PostPublishSuccessResponse):
    """Response body of successfully published a quest post."""


class QuestPostPublishFailedResponse(PostPublishFailedResponse):
    """Response body of failed to publish a quest post."""


# endregion


# region Quest Post / List

class QuestPostListResponseKey(PostListResponseKey):
    """
    Response keys of getting a quest post list.

    Keys must be consistent with the type ``QuestPostListResponse`` at the front side.
    """

    # These keys need to be consistent with the definition structure at the front side
    # Type name: `PostListEntry`
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
                cls.POSTS_LAST_MODIFIED: post[QuestPostKey.DT_LAST_MODIFIED],
                cls.POSTS_PUBLISHED: post[QuestPostKey.DT_PUBLISHED],
                cls.POSTS_VIEW_COUNT: post[QuestPostKey.VIEW_COUNT]
            })

        return ret


class QuestPostListResponse(PostListResponse):
    """Response body of getting a quest post list."""

    # pylint: disable=too-many-arguments
    def __init__(self, is_admin: bool, show_ads: bool, posts: list[dict[str, Any]], start_idx: int, post_count: int):
        super().__init__(is_admin, show_ads, start_idx, post_count)

        self._posts = QuestPostListResponseKey.convert_posts_key(posts)

    def serialize(self):
        return super().serialize() | {
            QuestPostListResponseKey.POSTS: self._posts
        }


# endregion


# region Quest Post / Get

class QuestPostGetSuccessResponseKey(PostGetSuccessResponseKey):
    """
    Response keys of getting a quest post.

    Keys must be consistent with the type ``QuestPostGetResponse`` at the front side.
    """

    TITLE = "title"

    GENERAL_INFO = "general"
    VIDEO = "video"

    INFO_PARENT = "info"
    INFO_POSITION = "position"
    INFO_BUILDS = "builds"
    INFO_ROTATIONS = "rotations"
    INFO_TIPS = "tips"

    ADDENDUM = "addendum"

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


class QuestPostGetSuccessResponse(PostGetSuccessResponse):
    """Response body of getting a quest post."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, is_admin: bool, show_ads: bool, get_result: MultilingualGetOneResult):
        super().__init__(is_admin, show_ads, get_result)

        post = get_result.data

        self._title = post[QuestPostKey.TITLE]
        self._general = post[QuestPostKey.GENERAL_INFO]
        self._video = post[QuestPostKey.VIDEO]
        self._info = QuestPostGetSuccessResponseKey.convert_info_key(post[QuestPostKey.INFO_PARENT])
        self._addendum = post[QuestPostKey.ADDENDUM]

    def serialize(self):
        return super().serialize() | {
            QuestPostGetSuccessResponseKey.TITLE: self._title,
            QuestPostGetSuccessResponseKey.GENERAL_INFO: self._general,
            QuestPostGetSuccessResponseKey.VIDEO: self._video,
            QuestPostGetSuccessResponseKey.INFO_PARENT: self._info,
            QuestPostGetSuccessResponseKey.ADDENDUM: self._addendum,
        }


class QuestPostGetFailedResponse(PostGetFailedResponse):
    """Response body of failed to get a quest post."""


# endregion


# region Quest Post / Edit

class QuestPostEditSuccessResponseKey(PostEditSuccessResponseKey):
    """Response keys of successfully edited a quest post."""


class QuestPostEditSuccessResponse(PostEditSuccessResponse):
    """Response body of successfully edited a quest post."""


class QuestPostEditFailedResponse(PostEditFailedResponse):
    """Response body of failed to edit a quest post."""


# endregion


# region Quest Post / ID Check

class QuestPostIDCheckResponseKey(PostIDCheckResponseKey):
    """Response keys of a quest post ID check request."""


class QuestPostIDCheckResponse(PostIDCheckResponse):
    """Response body of a quest post ID check request."""

# endregion
